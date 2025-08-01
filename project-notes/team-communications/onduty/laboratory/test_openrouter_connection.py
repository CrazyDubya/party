#!/usr/bin/env python3
"""
🧪 Quick OpenRouter API Connection Test
Verify the API key works before full integration
"""

import os
import asyncio
import aiohttp
import json

async def test_openrouter_connection():
    """Test OpenRouter API connection with minimal request"""
    
    api_key = os.getenv('OPENROUTER_API_KEY')
    if not api_key:
        print("❌ OPENROUTER_API_KEY not found in environment")
        return False
    
    print("🔍 Testing OpenRouter connection...")
    print(f"   API Key: {'✅ PROVIDED' if api_key else '❌ MISSING'}")
    print(f"   Key Preview: {api_key[:20]}..." if api_key else "   No key")
    
    # OpenRouter API endpoint
    url = "https://openrouter.ai/api/v1/chat/completions"
    
    # Minimal test request with cheapest model - match existing client format
    headers = {
        "Authorization": f"Bearer {api_key}",  # Use Bearer prefix like existing client
        "Content-Type": "application/json",
        "HTTP-Referer": "https://party-storyteller.app",  # Match existing client
        "X-Title": "AI Storytelling Engine"  # Match existing client
    }
    
    # Use a free model for testing (mistral-7b-instruct)
    data = {
        "model": "mistralai/mistral-7b-instruct:free",  # Free tier model
        "messages": [
            {"role": "user", "content": "Say 'API connection successful' in 5 words or less"}
        ],
        "max_tokens": 20,
        "temperature": 0.1
    }
    
    print(f"\n📤 Request Details:")
    print(f"   URL: {url}")
    print(f"   Model: {data['model']}")
    print(f"   Headers: {list(headers.keys())}")
    
    try:
        # Create connector with SSL disabled (same fix as ElevenLabs)
        connector = aiohttp.TCPConnector(ssl=False)
        async with aiohttp.ClientSession(connector=connector) as session:
            async with session.post(url, headers=headers, json=data) as response:
                if response.status == 200:
                    result = await response.json()
                    
                    print("\n✅ OpenRouter Connection SUCCESSFUL!")
                    print(f"   Status: {response.status}")
                    print(f"   Model Used: {result.get('model', 'unknown')}")
                    
                    # Extract response text
                    if 'choices' in result and len(result['choices']) > 0:
                        message = result['choices'][0]['message']['content']
                        print(f"   Response: {message}")
                    
                    # Show usage if available
                    if 'usage' in result:
                        print(f"   Tokens Used: {result['usage'].get('total_tokens', 0)}")
                    
                    return True
                else:
                    error_text = await response.text()
                    print(f"\n❌ Connection failed: {response.status}")
                    print(f"   Error: {error_text}")
                    return False
                    
    except Exception as e:
        print(f"\n❌ Connection error: {str(e)}")
        return False

async def list_available_models():
    """List available models from OpenRouter"""
    
    api_key = os.getenv('OPENROUTER_API_KEY')
    if not api_key:
        return
    
    print("\n📋 Fetching available models...")
    
    url = "https://openrouter.ai/api/v1/models"
    headers = {
        "Authorization": f"Bearer {api_key}",  # Use Bearer prefix like existing client
        "Content-Type": "application/json",
        "HTTP-Referer": "https://party-storyteller.app"
    }
    
    try:
        # Create connector with SSL disabled (same fix as ElevenLabs)
        connector = aiohttp.TCPConnector(ssl=False)
        async with aiohttp.ClientSession(connector=connector) as session:
            async with session.get(url, headers=headers) as response:
                if response.status == 200:
                    data = await response.json()
                    models = data.get('data', [])
                    
                    # Find free and cheap models
                    free_models = []
                    cheap_models = []
                    
                    for model in models:
                        model_id = model.get('id', '')
                        pricing = model.get('pricing', {})
                        
                        # Check if free
                        if ':free' in model_id or (pricing.get('prompt') == '0' and pricing.get('completion') == '0'):
                            free_models.append(model_id)
                        # Check if very cheap (< $0.0001 per 1k tokens)
                        elif pricing.get('prompt', '1') != '0':
                            prompt_cost = float(pricing.get('prompt', '1'))
                            if prompt_cost < 0.0001:
                                cheap_models.append((model_id, prompt_cost))
                    
                    print(f"\n🆓 Free Models Found: {len(free_models)}")
                    for model in free_models[:5]:  # Show first 5
                        print(f"   - {model}")
                    
                    print(f"\n💰 Ultra-Cheap Models: {len(cheap_models)}")
                    for model, cost in sorted(cheap_models, key=lambda x: x[1])[:5]:
                        print(f"   - {model} (${cost:.6f}/1k tokens)")
                    
    except Exception as e:
        print(f"❌ Error fetching models: {str(e)}")

async def main():
    """Run OpenRouter connection tests"""
    
    print("🚀 OPENROUTER CONNECTION TEST")
    print("=" * 50)
    
    # Test basic connection
    success = await test_openrouter_connection()
    
    if success:
        # List available models
        await list_available_models()
        
        print("\n🎉 OpenRouter is ready for Real AI integration!")
        print("   Next: Implement full text generation using real_api_integration_template.py")
    else:
        print("\n❌ OpenRouter connection failed. Check API key and try again.")

if __name__ == "__main__":
    asyncio.run(main())