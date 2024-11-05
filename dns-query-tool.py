import dns.resolver
import sys

def dns_query(domain, record_type):
    try:
        result = dns.resolver.resolve(domain, record_type)
        print(f"Results for {domain} ({record_type} records):")
        for ip in result:
            print(f" - {ip.to_text()}")
        return result

    except dns.resolver.NoAnswer:
        print(f"No answer for {domain} with record type {record_type}.")
    except dns.resolver.NXDOMAIN:
        print(f"The domain {domain} does not exist.")
    except dns.resolver.Timeout:
        print("DNS query timed out.")
    except Exception as e:
        print(f"An error occurred: {e}")

def save_results(domain, record_type, results):
    with open('dns_query_results.txt', 'a') as f:
        f.write(f"Results for {domain} ({record_type} records):\n")
        for ip in results:
            f.write(f" - {ip.to_text()}\n")
        f.write("\n")

def main():
    domain = input("Enter the domain name (e.g., example.com): ")
    record_type = input("Enter the DNS record type (A, AAAA, MX, TXT): ").upper()

    valid_record_types = ['A', 'AAAA', 'MX', 'TXT', 'CNAME', 'NS', 'PTR']
    if record_type not in valid_record_types:
        print(f"Invalid record type. Valid options are: {', '.join(valid_record_types)}")
        sys.exit(1)

    results = dns_query(domain, record_type)
    if results:
        save_results(domain, record_type, results)

if __name__ == "__main__":
    main()
