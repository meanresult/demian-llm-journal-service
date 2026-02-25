import os
from supabase import create_client
from dotenv import load_dotenv
load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_ANON_KEY = os.getenv("SUPABASE_ANON_KEY") 

email = "jihun_0420@naver.com"
password = "k03389801!"

supabase = create_client(SUPABASE_URL, SUPABASE_ANON_KEY)
res = supabase.auth.sign_in_with_password({"email": email, "password": password})

print(res.session.access_token)
