import boto.mturk.connection as conn
mturk = conn.MTurkConnection(aws_access_key_id='AKIAJUL53VTH3ENYMNIQ', aws_secret_access_key='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', is_secure=True, port=None, proxy=None, proxy_port=None, proxy_user=None, proxy_pass=None, host=None, debug=0, https_connection_factory=None, security_token=None, profile_name=None)
hits = mturk.get_all_hits()
for hit in hits:
    print hit
