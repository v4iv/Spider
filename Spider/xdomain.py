from urllib.parse import urlparse

#g Extract Domain Name
def get_domain(url):
    try:
        domain = get_sub_domain(url).split('.')
        return domain[-2] + '.' + domain[-1]
    except:
        return ''

# Extract Sub Domains
def get_sub_domain(url):
    try:
        return urlparse(url).netloc
    except:
        return ''
