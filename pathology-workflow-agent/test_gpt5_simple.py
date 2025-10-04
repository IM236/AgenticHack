#!/usr/bin/env python3
"""Simple GPT-5 test to find timeout issue."""

from dotenv import load_dotenv
load_dotenv('.env')

import asyncio
import time
from openai import OpenAI

async def test_direct_gpt5():
    """Test GPT-5 API directly."""
    print("Testing direct GPT-5 API call...")
    client = OpenAI()

    start = time.time()
    try:
        response = await asyncio.wait_for(
            asyncio.to_thread(
                lambda: client.responses.create(
                    model="gpt-5",
                    input="Say hello in 3 words or less"
                )
            ),
            timeout=10.0
        )
        elapsed = time.time() - start
        print(f"✓ Success in {elapsed:.2f}s: {response.output_text}")
        return True
    except asyncio.TimeoutError:
        elapsed = time.time() - start
        print(f"✗ TIMEOUT after {elapsed:.2f}s")
        return False
    except Exception as e:
        elapsed = time.time() - start
        print(f"✗ Error after {elapsed:.2f}s: {e}")
        return False


async def test_gpt5_wrapper():
    """Test our GPT-5 wrapper."""
    print("\nTesting GPT-5 wrapper...")
    import sys
    import os
    sys.path.insert(0, os.path.dirname(__file__))

    from src.utils.gpt5_client import GPT5Client
    from langchain_core.messages import SystemMessage, HumanMessage

    client = GPT5Client(api_key=os.getenv('OPENAI_API_KEY'), model='gpt-5')

    messages = [
        SystemMessage(content='Be brief'),
        HumanMessage(content='Say hello in 3 words')
    ]

    start = time.time()
    try:
        response = await asyncio.wait_for(
            client.ainvoke(messages),
            timeout=10.0
        )
        elapsed = time.time() - start
        print(f"✓ Success in {elapsed:.2f}s: {response}")
        return True
    except asyncio.TimeoutError:
        elapsed = time.time() - start
        print(f"✗ TIMEOUT after {elapsed:.2f}s")
        return False
    except Exception as e:
        elapsed = time.time() - start
        print(f"✗ Error after {elapsed:.2f}s: {e}")
        import traceback
        traceback.print_exc()
        return False


async def test_structured_output():
    """Test structured output."""
    print("\nTesting structured GPT-5 output...")
    import sys
    import os
    sys.path.insert(0, os.path.dirname(__file__))

    from src.utils.gpt5_client import GPT5Client
    from langchain_core.messages import SystemMessage, HumanMessage
    from pydantic import BaseModel, Field

    class SimpleResponse(BaseModel):
        greeting: str = Field(description="A simple greeting")

    client = GPT5Client(api_key=os.getenv('OPENAI_API_KEY'), model='gpt-5')
    structured_client = client.with_structured_output(SimpleResponse)

    messages = [
        SystemMessage(content='Be brief. Respond with JSON only.'),
        HumanMessage(content='Generate a greeting')
    ]

    start = time.time()
    try:
        response = await asyncio.wait_for(
            structured_client.ainvoke(messages),
            timeout=10.0
        )
        elapsed = time.time() - start
        print(f"✓ Success in {elapsed:.2f}s: {response.greeting}")
        return True
    except asyncio.TimeoutError:
        elapsed = time.time() - start
        print(f"✗ TIMEOUT after {elapsed:.2f}s")
        return False
    except Exception as e:
        elapsed = time.time() - start
        print(f"✗ Error after {elapsed:.2f}s: {e}")
        import traceback
        traceback.print_exc()
        return False


async def main():
    print("="*80)
    print("GPT-5 TIMEOUT DIAGNOSIS")
    print("="*80)

    # Test 1: Direct API
    result1 = await test_direct_gpt5()

    # Test 2: Wrapper
    result2 = await test_gpt5_wrapper()

    # Test 3: Structured output
    result3 = await test_structured_output()

    print("\n" + "="*80)
    print("RESULTS:")
    print(f"  Direct API: {'PASS' if result1 else 'FAIL'}")
    print(f"  Wrapper: {'PASS' if result2 else 'FAIL'}")
    print(f"  Structured: {'PASS' if result3 else 'FAIL'}")
    print("="*80)


if __name__ == "__main__":
    asyncio.run(main())
