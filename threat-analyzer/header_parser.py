import re
import dns.resolver

def check_domain_security(domain: str):
    print(f"\n?? Analyzing Authentication Matrix for: {domain}")
    print("-" * 50)
    
    # 1. Check SPF Record (Sender Policy Framework)
    try:
        spf_records = dns.resolver.resolve(domain, 'TXT')
        spf_found = False
        for record in spf_records:
            txt_data = record.to_text()
            if "v=spf1" in txt_data:
                print(f"? SPF Record Found: {txt_data}")
                spf_found = True
        if not spf_found:
            print("?? CRITICAL: No SPF record found! Senders can spoof this domain easily.")
    except Exception as e:
        print(f"?? Error fetching SPF: {e}")
        
    # 2. Check DMARC Policy (Domain-based Message Authentication)
    dmarc_domain = f"_dmarc.{domain}"
    try:
        dmarc_records = dns.resolver.resolve(dmarc_domain, 'TXT')
        for record in dmarc_records:
            txt_data = record.to_text()
            if "v=DMARC1" in txt_data:
                print(f"? DMARC Policy Found: {txt_data}")
                if "p=reject" in txt_data:
                    print("?? Strong Protection: Policy set to REJECT spoofed emails.")
                elif "p=quarantine" in txt_data:
                    print("?? Moderate Protection: Policy set to QUARANTINE suspicious emails.")
                else:
                    print("?? Weak Protection: Policy set to NONE. Spoofed emails will still land in inboxes.")
    except Exception:
        print("?? CRITICAL: No DMARC record found! Domain lacks anti-spoofing alignment enforcement.")

if __name__ == "__main__":
    # Test a major domain live
    check_domain_security("google.com")
