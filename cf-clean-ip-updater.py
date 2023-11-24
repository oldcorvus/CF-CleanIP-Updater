import random
import time
import argparse
from typing import List
from pydantic import BaseModel
import requests
import os

class Config:
    arbitrary_types_allowed = True

class CloudflareConfig(BaseModel):
    email: str
    api_key: str
    zone_id: str

class DomainIPConfig(BaseModel):
    domains_file: str
    ips_file: str
    duration: int

class CloudflareUpdater:
    def __init__(self, cloudflare_config: CloudflareConfig, target_domains):
        self.cloudflare_config = cloudflare_config
        self.api_url = f'https://api.cloudflare.com/client/v4/zones/{self.cloudflare_config.zone_id}/dns_records/'
        self.domain_identifier_dict = self.create_domain_identifier_dict(target_domains)
        
    def update_dns_record(self, domain: str,identifer:str, ip: str):
        headers = {
            'X-Auth-Email': self.cloudflare_config.email,
            'X-Auth-Key': self.cloudflare_config.api_key,
            'Content-Type': 'application/json',
        }

        data = {
            'type': 'A',
            'name': domain,
            'content': ip,
            'proxied': True
        }

        response = requests.put(self.api_url +f"/{identifer}", headers=headers, json=data)

        if response.status_code == 200:
            print(f"Successfully updated DNS record for {domain}")
        else:
            print(f"Failed to update DNS record for {domain}. Error: {response.text}")

    def update_domains(self, ips: List[str], duration: int):
        
        while True:
            for domain, identifer in self.domain_identifier_dict.items():
                ip = random.choice(ips)

                self.update_dns_record(domain, identifer , ip)

                time.sleep(duration)  #  delay to avoid rate limiting

    def _list_dns_records(self):

        headers = {
            'X-Auth-Email': self.cloudflare_config.email,
            'X-Auth-Key': self.cloudflare_config.api_key,
            'Content-Type': 'application/json',
        }

        response = requests.get(self.api_url, headers=headers)

        if response.status_code == 200:
            return response.json().get('result', [])
        else:
            print(f"Failed to list DNS records. Error: {response.text}")
            return []
        
    def create_domain_identifier_dict(self,  target_domains: List[str]):
        dns_records = self._list_dns_records()
        return {record['name']: record['id'] for record in dns_records if record['name'] in target_domains}

def parse_args():
    parser = argparse.ArgumentParser(description="Moel Cloudflare DNS Updater CLI")
    parser.add_argument("-e", "--email", required=True, help="Cloudflare account email")
    parser.add_argument("-k", "--api-key", required=True, help="Cloudflare API key")
    parser.add_argument("-z", "--zone-id", required=True, help="Cloudflare Zone ID")
    parser.add_argument("-df", "--domains-file", required=True, help="File containing a list of domains")
    parser.add_argument("-if", "--ips-file", required=True, help="File containing a list of IPs")
    parser.add_argument("-dr", "--duration", type=int, default=300, help="Duration in seconds (default is 300)")

    return parser.parse_args()

if __name__ == "__main__":
    args = parse_args()

    cloudflare_config = CloudflareConfig(
        email=args.email,
        api_key=args.api_key,
        zone_id=args.zone_id,
    )
    script_dir = os.path.dirname(os.path.abspath(__file__))

    domains_file_path = os.path.join(script_dir, args.domains_file) if args.domains_file else None
    ips_file_path = os.path.join(script_dir, args.ips_file) if args.ips_file else None

    with open(domains_file_path) as f:
        domains = [line.strip() for line in f]

    with open(ips_file_path) as f:
        ips = [line.strip() for line in f]

    updater = CloudflareUpdater(cloudflare_config, domains)
    updater.update_domains( ips, args.duration)
