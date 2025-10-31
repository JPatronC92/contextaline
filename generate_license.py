import hashlib
import random
import string

def checksum(payload):
    return hashlib.sha1(payload.encode()).hexdigest()[:6].upper()

def generate_license():
    for _ in range(1000):
        block1 = ''.join(random.choices(string.ascii_uppercase + string.digits, k=4))
        block2 = ''.join(random.choices(string.ascii_uppercase + string.digits, k=4))
        block3 = ''.join(random.choices(string.ascii_uppercase + string.digits, k=4))
        
        license_key = f'JDL-{block1}-{block2}-{block3}'
        core = license_key.replace('JDL-', '').replace('-', '')
        
        if checksum(core)[0] in 'ABCDEF':
            return license_key
    return None

if __name__ == "__main__":
    print("\n" + "="*50)
    print("GENERADOR DE LICENCIAS - IntelligentDocumentFinder")
    print("="*50)
    
    for i in range(5):
        lic = generate_license()
        if lic:
            print(f"\nLicencia #{i+1}: {lic}")
    
    print("\n" + "="*50)
    print("Copia cualquiera de estas licencias en la aplicación")
    print("="*50)
