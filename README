# Cloudflare Clean IP Updater

This is a Python application that updates Cloudflare DNS records with new IP addresses.

## How to Use

### Prerequisites
- Python installed on your machine

### Getting Started

1. **Clone the Repository:**
   ```bash
    git clone https://github.com/oldcorvus/CF-CleanIP-Updater.git
    cd CF-CleanIP-Updater
    pip install -r requirements.txt
   ```

2. **Set Up Cloudflare API Token**:

    Log in to your Cloudflare account.
    Go to the API Tokens page.
    Create a new API Token with the necessary permissions (e.g., Zone:DNS:Edit).
    Note down the API Token.

3. **Get Zone ID**:

    Go to the Cloudflare Dashboard.
    Select the domain for which you want to get the Zone ID.
    The Zone ID should be visible in the Overview section.

4. **Create Files for Domains and IPs**:

    Create a file named domains.txt containing the list of domains, each on a new line.
    Create a file named ips.txt containing the list of IP addresses, each on a new line.

5. **Run the Application**:

   ```bash
    python cf-clean-ip-updater.py -e youremail -z your-zoneid -k your-api-token -df domains.txt -if ips.txt -dr your-duration
   ```
    example:
      python cf-clean-ip-updater.py -e moelcrow@gmail.com -z 8efa5b78f5fc6702ea3beb58510c2fe3 -k 1f2baf69f83d91393bacf957ac2b627dcd227 -df domains.txt -if ips.txt -dr 10