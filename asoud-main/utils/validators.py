import re
import uuid
from django.core.exceptions import ValidationError
from decimal import Decimal, InvalidOperation
import html
import unicodedata


def validate_mobile_number(mobile_number):
    """
    Ruthless Iranian mobile number validation
    """
    if not mobile_number:
        raise ValidationError("Mobile number is required")
    
    # Remove any whitespace or special characters
    mobile_number = re.sub(r'[^\d]', '', str(mobile_number))
    
    # Aggressive validation for Iranian networks
    iranian_prefixes = [
        '0901', '0902', '0903', '0905', '0990', '0991', '0992', '0993', '0994',
        '0995', '0996', '0997', '0998', '0999', '0910', '0911', '0912', '0913',
        '0914', '0915', '0916', '0917', '0918', '0919', '0920', '0921', '0922'
    ]
    
    if not any(mobile_number.startswith(prefix) for prefix in iranian_prefixes):
        raise ValidationError("Invalid Iranian mobile network prefix")
    
    if len(mobile_number) != 11:
        raise ValidationError("Mobile number must be exactly 11 digits")
    
    # Block suspicious patterns
    if mobile_number[2:] == '000000000' or len(set(mobile_number)) < 3:
        raise ValidationError("Invalid mobile number pattern")
    
    return mobile_number


def validate_pin_code(pin):
    """
    Ruthless PIN validation
    """
    if not pin:
        raise ValidationError("PIN code is required")
    
    pin_str = str(pin).strip()
    
    if not re.match(r'^\d{4}$', pin_str):
        raise ValidationError("PIN must be exactly 4 digits")
    
    # Block weak PINs
    weak_pins = ['0000', '1111', '2222', '3333', '4444', '5555', '6666', '7777', '8888', '9999',
                 '1234', '4321', '0123', '9876', '1357', '2468']
    if pin_str in weak_pins:
        raise ValidationError("PIN is too weak, choose a different combination")
    
    return pin_str


def validate_amount(amount):
    """
    Ruthless monetary amount validation
    """
    if amount is None:
        raise ValidationError("Amount is required")
    
    try:
        amount = Decimal(str(amount))
        if amount <= 0:
            raise ValidationError("Amount must be positive")
        if amount > Decimal('999999999999.99'):  # Trillion limit
            raise ValidationError("Amount exceeds maximum limit")
        if amount < Decimal('0.01'):  # Minimum 1 cent
            raise ValidationError("Amount too small")
        
        # Check for suspicious round numbers in large amounts
        if amount > Decimal('1000000') and amount % Decimal('1000000') == 0:
            raise ValidationError("Suspicious round amount detected")
            
        return amount
    except (InvalidOperation, ValueError):
        raise ValidationError("Invalid amount format")


def validate_uuid_format(uuid_string):
    """
    Ruthless UUID validation
    """
    if not uuid_string:
        raise ValidationError("UUID is required")
    
    try:
        parsed_uuid = uuid.UUID(str(uuid_string))
        # Ensure it's not a nil UUID
        if parsed_uuid.int == 0:
            raise ValidationError("Nil UUID not allowed")
        return str(parsed_uuid)
    except ValueError:
        raise ValidationError("Invalid UUID format")


def validate_business_id(business_id):
    """
    Ruthless business ID validation for subdomain security
    """
    if not business_id:
        raise ValidationError("Business ID is required")
    
    business_id = str(business_id).strip().lower()
    
    # Strict alphanumeric with dash/underscore only
    if not re.match(r'^[a-z0-9_-]{3,20}$', business_id):
        raise ValidationError("Business ID must be 3-20 characters, alphanumeric with dash/underscore only")
    
    # Block reserved words
    reserved_words = [
        'admin', 'api', 'www', 'mail', 'ftp', 'localhost', 'test', 'dev', 'staging',
        'production', 'app', 'web', 'server', 'database', 'db', 'root', 'user',
        'asoud', 'payment', 'login', 'register', 'dashboard', 'panel', 'control',
        'support', 'help', 'about', 'contact', 'blog', 'news', 'shop', 'store'
    ]
    
    if business_id in reserved_words:
        raise ValidationError("Business ID conflicts with reserved word")
    
    # Block sequential patterns
    if re.search(r'(012|123|234|345|456|567|678|789|abc|def|ghi)', business_id):
        raise ValidationError("Business ID contains sequential pattern")
    
    return business_id


def validate_iban(iban):
    """
    Ruthless Iranian IBAN validation
    """
    if not iban:
        raise ValidationError("IBAN is required")
    
    iban = re.sub(r'[^0-9A-Z]', '', str(iban).upper())
    
    # Iranian IBAN format: IR + 2 check digits + 22 digits
    if not re.match(r'^IR\d{24}$', iban):
        raise ValidationError("Invalid Iranian IBAN format")
    
    # Basic IBAN checksum validation
    rearranged = iban[4:] + iban[:4]
    numeric = ''.join(str(ord(char) - ord('A') + 10) if char.isalpha() else char for char in rearranged)
    
    if int(numeric) % 97 != 1:
        raise ValidationError("Invalid IBAN checksum")
    
    return iban


def sanitize_input(input_string):
    """
    Ruthless input sanitization
    """
    if input_string is None:
        return None
    
    # Convert to string and normalize Unicode
    sanitized = unicodedata.normalize('NFKC', str(input_string))
    
    # HTML escape
    sanitized = html.escape(sanitized)
    
    # Strip whitespace
    sanitized = sanitized.strip()
    
    # Remove control characters except tab, newline, carriage return
    sanitized = ''.join(char for char in sanitized if ord(char) >= 32 or char in '\t\n\r')
    
    # Block script injections
    dangerous_patterns = [
        r'<script[^>]*>.*?</script>',
        r'javascript:',
        r'vbscript:',
        r'onload\s*=',
        r'onerror\s*=',
        r'onclick\s*=',
        r'eval\s*\(',
        r'expression\s*\(',
        r'\\x[0-9a-fA-F]{2}',  # Hex encoding
        r'&#x[0-9a-fA-F]+;',   # Hex entities
    ]
    
    for pattern in dangerous_patterns:
        sanitized = re.sub(pattern, '', sanitized, flags=re.IGNORECASE)
    
    # Limit length
    if len(sanitized) > 1000:
        sanitized = sanitized[:1000]
    
    return sanitized


def validate_persian_text(text, min_length=1, max_length=255):
    """
    Validate Persian text input
    """
    if not text:
        raise ValidationError("Persian text is required")
    
    text = sanitize_input(text)
    
    if len(text) < min_length:
        raise ValidationError(f"Text must be at least {min_length} characters")
    
    if len(text) > max_length:
        raise ValidationError(f"Text must not exceed {max_length} characters")
    
    # Allow Persian, Arabic, English, numbers, and common punctuation
    allowed_pattern = r'^[\u0600-\u06FF\u0750-\u077F\u08A0-\u08FF\uFB50-\uFDFF\uFE70-\uFEFFa-zA-Z0-9\s\.\,\!\?\-\(\)]+$'
    
    if not re.match(allowed_pattern, text):
        raise ValidationError("Text contains invalid characters")
    
    return text