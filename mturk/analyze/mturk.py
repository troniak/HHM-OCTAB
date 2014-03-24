import boto.mturk.connection as conn

qualified_workers = ['A248D5XVN1YGCZ', 'A2QAJ8BJ5QBB9A', 'A2WRSEO8HQRG5K', 'A37P0EXFVTAP0D', 'A38KIO2400LOTJ', 'A3DY78Q4FCWTXX', 'A3N87BX6PS0SIB', 'A9XWAWNLJN8DA']
action_annotation_type_id = '276M25L8I9N3M15OL9FEFQW7T8OIS7'

def new_mturk_connection():
    return conn.MTurkConnection(aws_access_key_id='AKIAJUL53VTH3ENYMNIQ', aws_secret_access_key='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', is_secure=True, port=None, proxy=None, proxy_port=None, proxy_user=None, proxy_pass=None, host=None, debug=0, https_connection_factory=None, security_token=None, profile_name=None)
