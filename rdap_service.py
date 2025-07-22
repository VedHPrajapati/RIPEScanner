import ipaddress
import requests
import logging
from datetime import datetime
from typing import Dict, Any, Union

class RDAPService:
    """Service for handling RDAP lookups with automatic RIR detection"""
    
    def __init__(self):
        # RDAP endpoints for different RIRs
        self.rdap_endpoints = {
            'ARIN': 'https://rdap.arin.net/registry/ip/',
            'RIPE': 'https://rdap.db.ripe.net/ip/',
            'APNIC': 'https://rdap.apnic.net/ip/',
            'LACNIC': 'https://rdap.lacnic.net/rdap/ip/',
            'AFRINIC': 'https://rdap.afrinic.net/rdap/ip/'
        }
        
        # IP ranges for each RIR (simplified ranges for demonstration)
        # In production, you would use IANA's bootstrap registry
        self.rir_ranges = {
            'ARIN': [
                # North America
                '3.0.0.0/8', '4.0.0.0/8', '6.0.0.0/8', '7.0.0.0/8', '8.0.0.0/8',
                '9.0.0.0/8', '11.0.0.0/8', '12.0.0.0/8', '13.0.0.0/8', '15.0.0.0/8',
                '16.0.0.0/8', '17.0.0.0/8', '18.0.0.0/8', '19.0.0.0/8', '20.0.0.0/8',
                '21.0.0.0/8', '22.0.0.0/8', '23.0.0.0/8', '24.0.0.0/8', '26.0.0.0/8',
                '28.0.0.0/8', '29.0.0.0/8', '30.0.0.0/8', '32.0.0.0/8', '33.0.0.0/8',
                '34.0.0.0/8', '35.0.0.0/8', '38.0.0.0/8', '40.0.0.0/8', '44.0.0.0/8',
                '47.0.0.0/8', '48.0.0.0/8', '50.0.0.0/8', '52.0.0.0/8', '54.0.0.0/8',
                '55.0.0.0/8', '56.0.0.0/8', '63.0.0.0/8', '64.0.0.0/8', '65.0.0.0/8',
                '66.0.0.0/8', '67.0.0.0/8', '68.0.0.0/8', '69.0.0.0/8', '70.0.0.0/8',
                '71.0.0.0/8', '72.0.0.0/8', '73.0.0.0/8', '74.0.0.0/8', '75.0.0.0/8',
                '76.0.0.0/8', '96.0.0.0/8', '97.0.0.0/8', '98.0.0.0/8', '99.0.0.0/8',
                '100.0.0.0/8', '104.0.0.0/8', '107.0.0.0/8', '108.0.0.0/8', '173.0.0.0/8',
                '174.0.0.0/8', '184.0.0.0/8', '192.0.0.0/8', '198.0.0.0/8', '199.0.0.0/8',
                '204.0.0.0/8', '205.0.0.0/8', '206.0.0.0/8', '207.0.0.0/8', '208.0.0.0/8',
                '209.0.0.0/8', '216.0.0.0/8',
                # IPv6 ranges for ARIN
                '2001:400::/23', '2001:1800::/23', '2600::/12', '2610::/23', '2620::/23'
            ],
            'RIPE': [
                # Europe, Middle East, Central Asia
                '2.0.0.0/8', '5.0.0.0/8', '25.0.0.0/8', '31.0.0.0/8', '37.0.0.0/8',
                '46.0.0.0/8', '51.0.0.0/8', '53.0.0.0/8', '57.0.0.0/8', '62.0.0.0/8',
                '77.0.0.0/8', '78.0.0.0/8', '79.0.0.0/8', '80.0.0.0/8', '81.0.0.0/8',
                '82.0.0.0/8', '83.0.0.0/8', '84.0.0.0/8', '85.0.0.0/8', '86.0.0.0/8',
                '87.0.0.0/8', '88.0.0.0/8', '89.0.0.0/8', '90.0.0.0/8', '91.0.0.0/8',
                '92.0.0.0/8', '93.0.0.0/8', '94.0.0.0/8', '95.0.0.0/8', '109.0.0.0/8',
                '176.0.0.0/8', '178.0.0.0/8', '185.0.0.0/8', '188.0.0.0/8', '193.0.0.0/8',
                '194.0.0.0/8', '195.0.0.0/8', '212.0.0.0/8', '213.0.0.0/8', '217.0.0.0/8',
                # IPv6 ranges for RIPE
                '2001:600::/23', '2001:1400::/23', '2001:2000::/19', '2a00::/12'
            ],
            'APNIC': [
                # Asia Pacific
                '1.0.0.0/8', '14.0.0.0/8', '27.0.0.0/8', '36.0.0.0/8', '39.0.0.0/8',
                '42.0.0.0/8', '43.0.0.0/8', '49.0.0.0/8', '58.0.0.0/8', '59.0.0.0/8',
                '60.0.0.0/8', '61.0.0.0/8', '101.0.0.0/8', '103.0.0.0/8', '106.0.0.0/8',
                '110.0.0.0/8', '111.0.0.0/8', '112.0.0.0/8', '113.0.0.0/8', '114.0.0.0/8',
                '115.0.0.0/8', '116.0.0.0/8', '117.0.0.0/8', '118.0.0.0/8', '119.0.0.0/8',
                '120.0.0.0/8', '121.0.0.0/8', '122.0.0.0/8', '123.0.0.0/8', '124.0.0.0/8',
                '125.0.0.0/8', '126.0.0.0/8', '133.0.0.0/8', '150.0.0.0/8', '153.0.0.0/8',
                '163.0.0.0/8', '171.0.0.0/8', '175.0.0.0/8', '180.0.0.0/8', '182.0.0.0/8',
                '183.0.0.0/8', '202.0.0.0/8', '203.0.0.0/8', '210.0.0.0/8', '211.0.0.0/8',
                '218.0.0.0/8', '219.0.0.0/8', '220.0.0.0/8', '221.0.0.0/8', '222.0.0.0/8',
                '223.0.0.0/8',
                # IPv6 ranges for APNIC
                '2001:200::/23', '2001:c00::/23', '2400::/12'
            ],
            'LACNIC': [
                # Latin America and Caribbean
                '177.0.0.0/8', '179.0.0.0/8', '181.0.0.0/8', '186.0.0.0/8', '187.0.0.0/8',
                '189.0.0.0/8', '190.0.0.0/8', '191.0.0.0/8', '200.0.0.0/8', '201.0.0.0/8',
                # IPv6 ranges for LACNIC
                '2001:1200::/23', '2800::/12'
            ],
            'AFRINIC': [
                # Africa
                '41.0.0.0/8', '102.0.0.0/8', '105.0.0.0/8', '154.0.0.0/8', '155.0.0.0/8',
                '156.0.0.0/8', '196.0.0.0/8', '197.0.0.0/8',
                # IPv6 ranges for AFRINIC
                '2001:4200::/23', '2c00::/12'
            ]
        }
    
    def validate_ip(self, ip_input: str) -> Dict[str, Any]:
        """Validate IP address or network"""
        try:
            # Try to parse as network first
            if '/' in ip_input:
                network = ipaddress.ip_network(ip_input, strict=False)
                return {
                    'valid': True,
                    'type': 'network',
                    'version': network.version,
                    'message': f'Valid IPv{network.version} network: {network}'
                }
            else:
                # Try to parse as IP address
                ip = ipaddress.ip_address(ip_input)
                return {
                    'valid': True,
                    'type': 'address',
                    'version': ip.version,
                    'message': f'Valid IPv{ip.version} address: {ip}'
                }
        except ValueError as e:
            return {
                'valid': False,
                'message': f'Invalid IP address or network: {str(e)}'
            }
    
    def detect_rir(self, ip_input: str) -> str:
        """Detect which RIR should handle this IP address"""
        try:
            # Parse the input
            if '/' in ip_input:
                # It's a network, get the first IP
                network = ipaddress.ip_network(ip_input, strict=False)
                ip = network.network_address
            else:
                # It's an IP address
                ip = ipaddress.ip_address(ip_input)
            
            # Check against each RIR's ranges
            for rir, ranges in self.rir_ranges.items():
                for range_str in ranges:
                    try:
                        range_network = ipaddress.ip_network(range_str)
                        if ip in range_network:
                            return rir
                    except ValueError:
                        continue
            
            # Default fallback - try ARIN first for unknown ranges
            return 'ARIN'
            
        except ValueError:
            # If we can't parse the IP, default to ARIN
            return 'ARIN'
    
    def query_rdap(self, ip_input: str, rir: str) -> Dict[str, Any]:
        """Query RDAP endpoint for the given IP and RIR"""
        try:
            # Extract IP address from input
            if '/' in ip_input:
                network = ipaddress.ip_network(ip_input, strict=False)
                ip = str(network.network_address)
            else:
                ip = str(ipaddress.ip_address(ip_input))
            
            # Construct RDAP URL
            base_url = self.rdap_endpoints.get(rir)
            if not base_url:
                return {'error': f'Unknown RIR: {rir}'}
            
            url = f"{base_url}{ip}"
            
            # Make the request
            logging.info(f"Querying RDAP: {url}")
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            
            return response.json()
            
        except requests.exceptions.RequestException as e:
            logging.error(f"RDAP request failed: {str(e)}")
            return {'error': f'RDAP request failed: {str(e)}'}
        except Exception as e:
            logging.error(f"Unexpected error in RDAP query: {str(e)}")
            return {'error': f'Unexpected error: {str(e)}'}
    
    def format_rdap_response(self, rdap_data: Dict[str, Any], rir: str) -> Dict[str, Any]:
        """Format RDAP response for display"""
        if 'error' in rdap_data:
            return rdap_data
        
        formatted = {
            'rir': rir,
            'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S UTC'),
            'raw_data': rdap_data
        }
        
        # Extract key information
        if 'name' in rdap_data:
            formatted['network_name'] = rdap_data['name']
        
        if 'startAddress' in rdap_data and 'endAddress' in rdap_data:
            formatted['ip_range'] = f"{rdap_data['startAddress']} - {rdap_data['endAddress']}"
        
        if 'cidr0_cidrs' in rdap_data:
            formatted['cidr_blocks'] = rdap_data['cidr0_cidrs']
        
        # Extract organization information
        if 'entities' in rdap_data:
            for entity in rdap_data['entities']:
                if 'roles' in entity and 'registrant' in entity['roles']:
                    if 'vcardArray' in entity:
                        formatted['organization'] = self.parse_vcard(entity['vcardArray'])
                    break
        
        # Extract contact information
        formatted['contacts'] = []
        if 'entities' in rdap_data:
            for entity in rdap_data['entities']:
                if 'roles' in entity:
                    contact = {
                        'roles': entity['roles'],
                        'handle': entity.get('handle', 'N/A')
                    }
                    if 'vcardArray' in entity:
                        contact.update(self.parse_vcard(entity['vcardArray']))
                    formatted['contacts'].append(contact)
        
        return formatted
    
    def parse_vcard(self, vcard_array: list) -> Dict[str, str]:
        """Parse vCard data from RDAP response"""
        vcard_info = {}
        
        if len(vcard_array) < 2:
            return vcard_info
        
        vcard_data = vcard_array[1]
        
        for item in vcard_data:
            if len(item) >= 4:
                field_name = item[0].lower()
                field_value = item[3]
                
                if field_name == 'fn':
                    vcard_info['name'] = field_value
                elif field_name == 'org':
                    vcard_info['organization'] = field_value
                elif field_name == 'email':
                    vcard_info['email'] = field_value
                elif field_name == 'tel':
                    vcard_info['phone'] = field_value
                elif field_name == 'adr':
                    if isinstance(field_value, list):
                        address_parts = [part for part in field_value if part]
                        vcard_info['address'] = ', '.join(address_parts)
                    else:
                        vcard_info['address'] = field_value
        
        return vcard_info
    
    def lookup(self, ip_input: str) -> Dict[str, Any]:
        """Perform complete RDAP lookup"""
        # Validate input
        validation = self.validate_ip(ip_input)
        if not validation['valid']:
            return {'error': validation['message']}
        
        # Detect RIR
        rir = self.detect_rir(ip_input)
        
        # Query RDAP
        rdap_data = self.query_rdap(ip_input, rir)
        
        # Format response
        return self.format_rdap_response(rdap_data, rir)


class GeolocationService:
    """Service for IP geolocation intelligence"""
    
    def __init__(self):
        # Using ipinfo.io as the primary geolocation service
        self.ipinfo_url = "http://ipinfo.io/{}/json"
        
    def get_location_data(self, ip_address: str) -> Dict[str, Any]:
        """Get geolocation data for an IP address"""
        try:
            # Clean IP address (remove CIDR notation if present)
            clean_ip = ip_address.split('/')[0]
            
            # Validate IP address
            ipaddress.ip_address(clean_ip)
            
            # Query ipinfo.io for geolocation data
            url = self.ipinfo_url.format(clean_ip)
            response = requests.get(url, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                
                # Extract coordinates if available
                coordinates = {}
                if 'loc' in data:
                    try:
                        lat, lon = data['loc'].split(',')
                        coordinates = {
                            'latitude': float(lat),
                            'longitude': float(lon)
                        }
                    except:
                        coordinates = {}
                
                return {
                    'ip': clean_ip,
                    'city': data.get('city', 'Unknown'),
                    'region': data.get('region', 'Unknown'),
                    'country': data.get('country', 'Unknown'),
                    'country_name': self._get_country_name(data.get('country', '')),
                    'timezone': data.get('timezone', 'Unknown'),
                    'coordinates': coordinates,
                    'postal': data.get('postal', 'Unknown'),
                    'asn': data.get('org', 'Unknown'),
                    'success': True
                }
            else:
                return {'success': False, 'error': f'Geolocation service returned status {response.status_code}'}
                
        except Exception as e:
            logging.error(f"Geolocation lookup failed: {str(e)}")
            return {'success': False, 'error': f'Geolocation lookup failed: {str(e)}'}
    
    def _get_country_name(self, country_code: str) -> str:
        """Convert country code to full country name"""
        country_names = {
            'US': 'United States', 'CA': 'Canada', 'GB': 'United Kingdom',
            'DE': 'Germany', 'FR': 'France', 'JP': 'Japan', 'CN': 'China',
            'IN': 'India', 'BR': 'Brazil', 'AU': 'Australia', 'RU': 'Russia',
            'IT': 'Italy', 'ES': 'Spain', 'KR': 'South Korea', 'NL': 'Netherlands',
            'SE': 'Sweden', 'NO': 'Norway', 'DK': 'Denmark', 'FI': 'Finland',
            'PL': 'Poland', 'CH': 'Switzerland', 'AT': 'Austria', 'BE': 'Belgium',
            'IE': 'Ireland', 'PT': 'Portugal', 'GR': 'Greece', 'CZ': 'Czech Republic',
            'HU': 'Hungary', 'RO': 'Romania', 'BG': 'Bulgaria', 'HR': 'Croatia',
            'SK': 'Slovakia', 'SI': 'Slovenia', 'EE': 'Estonia', 'LV': 'Latvia',
            'LT': 'Lithuania', 'LU': 'Luxembourg', 'MT': 'Malta', 'CY': 'Cyprus'
        }
        return country_names.get(country_code, country_code)


class ASNService:
    """Service for Autonomous System Number lookups"""
    
    def __init__(self):
        self.asn_api_url = "https://api.hackertarget.com/aslookup/?q={}"
        
    def get_asn_data(self, ip_address: str) -> Dict[str, Any]:
        """Get ASN information for an IP address"""
        try:
            # Clean IP address
            clean_ip = ip_address.split('/')[0]
            ipaddress.ip_address(clean_ip)
            
            # Query ASN lookup API
            url = self.asn_api_url.format(clean_ip)
            response = requests.get(url, timeout=10)
            
            if response.status_code == 200:
                asn_text = response.text.strip()
                
                if 'AS' in asn_text and not 'error' in asn_text.lower():
                    # Parse ASN response (format: "AS12345 ISP Name")
                    parts = asn_text.split(' ', 1)
                    asn_number = parts[0] if parts else 'Unknown'
                    asn_name = parts[1] if len(parts) > 1 else 'Unknown'
                    
                    return {
                        'ip': clean_ip,
                        'asn_number': asn_number,
                        'asn_name': asn_name,
                        'asn_full': asn_text,
                        'success': True
                    }
                else:
                    return {'success': False, 'error': 'ASN not found for this IP'}
            else:
                return {'success': False, 'error': f'ASN service returned status {response.status_code}'}
                
        except Exception as e:
            logging.error(f"ASN lookup failed: {str(e)}")
            return {'success': False, 'error': f'ASN lookup failed: {str(e)}'}


class BatchService:
    """Service for batch IP address processing"""
    
    def __init__(self, rdap_service: RDAPService):
        self.rdap_service = rdap_service
        self.geo_service = GeolocationService()
        self.asn_service = ASNService()
        
    def process_batch(self, ip_list: list) -> Dict[str, Any]:
        """Process multiple IP addresses in batch"""
        results = []
        errors = []
        
        for ip in ip_list:
            ip = ip.strip()
            if not ip:
                continue
                
            try:
                # Validate IP
                validation = self.rdap_service.validate_ip(ip)
                if not validation['valid']:
                    errors.append(f"{ip}: {validation['message']}")
                    continue
                
                # Basic RDAP lookup
                rdap_result = self.rdap_service.lookup(ip)
                
                # Enhanced data
                geo_data = self.geo_service.get_location_data(ip)
                asn_data = self.asn_service.get_asn_data(ip)
                
                result = {
                    'ip': ip,
                    'rdap': rdap_result,
                    'geolocation': geo_data,
                    'asn': asn_data,
                    'processed_at': datetime.now().isoformat()
                }
                
                results.append(result)
                
            except Exception as e:
                errors.append(f"{ip}: {str(e)}")
                
        return {
            'total_processed': len(results),
            'total_errors': len(errors),
            'results': results,
            'errors': errors,
            'success': len(results) > 0
        }
    
    def export_results(self, results: Dict[str, Any], format_type: str = 'json') -> str:
        """Export batch results in various formats"""
        if format_type == 'json':
            return json.dumps(results, indent=2)
        elif format_type == 'csv':
            return self._to_csv(results)
        else:
            return json.dumps(results, indent=2)
    
    def _to_csv(self, results: Dict[str, Any]) -> str:
        """Convert results to CSV format"""
        if not results.get('results'):
            return "No results to export"
        
        csv_lines = ['IP,RIR,Network,Organization,Country,ASN,ASN_Name,City,Region']
        
        for result in results['results']:
            ip = result.get('ip', '')
            rdap = result.get('rdap', {})
            geo = result.get('geolocation', {})
            asn = result.get('asn', {})
            
            line = [
                ip,
                rdap.get('rir', ''),
                rdap.get('network', ''),
                rdap.get('organization', ''),
                geo.get('country_name', ''),
                asn.get('asn_number', ''),
                asn.get('asn_name', ''),
                geo.get('city', ''),
                geo.get('region', '')
            ]
            
            # Clean and escape CSV values
            clean_line = [str(field).replace(',', ';').replace('\n', ' ') for field in line]
            csv_lines.append(','.join(clean_line))
        
        return '\n'.join(csv_lines)
