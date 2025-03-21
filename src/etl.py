from supabase import create_client
import pandas as pd
import os
from dotenv import load_dotenv

# Cargar variables desde .env
load_dotenv()
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")


