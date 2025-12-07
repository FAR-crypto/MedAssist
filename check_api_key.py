import os

print("=" * 80)
print("OPENAI API KEY ENVIRONMENT CHECK")
print("=" * 80)
print()

# Check session environment
key_session = os.environ.get('OPENAI_API_KEY')
print("1. SESSION ENVIRONMENT (Current PowerShell):")
print(f"   Status: {'✅ SET' if key_session else '❌ NOT SET'}")
if key_session:
    print(f"   Value: {key_session[:10]}...{key_session[-10:]}")
    print(f"   Length: {len(key_session)} characters")
else:
    print("   Value: NOT SET")
print()

# Check user-level environment variable (Windows Registry)
print("2. USER-LEVEL ENVIRONMENT (Windows Registry - Persistent):")
user_key = os.environ.get('OPENAI_API_KEY', None)
if user_key:
    print(f"   Status: ✅ SET")
    print(f"   Value: {user_key[:10]}...{user_key[-10:]}")
else:
    # Try to get from registry directly
    try:
        from winreg import ConnectRegistry, OpenKey, QueryValueEx, HKEY_CURRENT_USER
        hive = ConnectRegistry(None, HKEY_CURRENT_USER)
        key_obj = OpenKey(hive, r"Environment")
        user_env_key, _ = QueryValueEx(key_obj, "OPENAI_API_KEY")
        print(f"   Status: ✅ SET (in registry)")
        print(f"   Value: {user_env_key[:10]}...{user_env_key[-10:]}")
        print(f"   Note: Not loaded in current session. Restart PowerShell to load.")
    except Exception as e:
        print(f"   Status: ❌ NOT SET")
        print(f"   Error: {str(e)}")
print()

# Check if OpenAI package can access the key
print("3. OPENAI PACKAGE TEST:")
try:
    import openai
    if os.environ.get('OPENAI_API_KEY'):
        openai.api_key = os.environ.get('OPENAI_API_KEY')
        print("   Status: ✅ OPENAI PACKAGE CAN USE KEY")
        print(f"   OpenAI version: {openai.__version__}")
    else:
        print("   Status: ⚠️  Key not in session")
        print("   Fix: Load key into session with: $env:OPENAI_API_KEY = [Environment]::GetEnvironmentVariable('OPENAI_API_KEY', 'User')")
except ImportError:
    print("   Status: ❌ OpenAI package not installed")
print()

print("=" * 80)
print("RECOMMENDATIONS:")
print("=" * 80)
if key_session:
    print("✅ API Key is loaded and ready to use!")
    print("   Backend can access OpenAI API now.")
else:
    print("❌ API Key NOT loaded in current session")
    print()
    print("To fix, run in PowerShell:")
    print("  $env:OPENAI_API_KEY = [Environment]::GetEnvironmentVariable('OPENAI_API_KEY', 'User')")
    print()
    print("Or to set permanently (for next session):")
    print("  setx OPENAI_API_KEY \"sk-your-actual-key-here\"")
print()
