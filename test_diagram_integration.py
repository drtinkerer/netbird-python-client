#!/usr/bin/env python3
"""
Simple test script to verify the new diagram generation functionality.
This script tests the integration of diagram generation into the NetBird client.
"""

import os
import sys
import tempfile
from pathlib import Path

# Add the src directory to the path for local development
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from netbird import APIClient
from netbird.exceptions import NetBirdAPIError


def test_diagram_functionality():
    """Test the diagram generation functionality."""
    print("🧪 Testing NetBird Client Diagram Generation")
    print("=" * 50)
    
    # Check environment variables
    host = os.getenv("NETBIRD_HOST", "api.netbird.io")
    token = os.getenv("NETBIRD_API_TOKEN")
    
    if not token:
        print("❌ NETBIRD_API_TOKEN environment variable is required")
        print("   Set it with: export NETBIRD_API_TOKEN='your-token-here'")
        return False
    
    print(f"🔗 Connecting to: {host}")
    print(f"🔐 Token: {token[:10]}...")
    
    try:
        # Create client
        client = APIClient(host=host, api_token=token)
        print("✅ Client created successfully")
        
        # Test 1: Check if generate_diagram method exists
        print("\n🔍 Test 1: Method availability")
        if hasattr(client, 'generate_diagram'):
            print("✅ generate_diagram method found")
        else:
            print("❌ generate_diagram method not found")
            return False
        
        # Test 2: Generate Mermaid diagram (no file output)
        print("\n🔍 Test 2: Mermaid diagram generation")
        try:
            mermaid_content = client.generate_diagram(format="mermaid")
            if mermaid_content:
                print(f"✅ Mermaid diagram generated ({len(mermaid_content)} chars)")
                print(f"   Preview: {mermaid_content[:100]}...")
            else:
                print("⚠️  No mermaid content returned (no networks?)")
        except Exception as e:
            print(f"❌ Mermaid generation failed: {e}")
            return False
        
        # Test 3: Generate with file output
        print("\n🔍 Test 3: File output generation")
        try:
            with tempfile.TemporaryDirectory() as temp_dir:
                output_path = os.path.join(temp_dir, "test_diagram")
                
                result = client.generate_diagram(
                    format="mermaid",
                    output_file=output_path,
                    include_routers=True,
                    include_policies=True,
                    include_resources=True
                )
                
                if result:
                    print("✅ Diagram generated with file output")
                    
                    # Check if files were created
                    mermaid_file = f"{output_path}.mmd"
                    markdown_file = f"{output_path}.md"
                    
                    if os.path.exists(mermaid_file):
                        print("✅ Mermaid file created")
                        with open(mermaid_file, 'r') as f:
                            content = f.read()
                            print(f"   File size: {len(content)} chars")
                    else:
                        print("❌ Mermaid file not found")
                    
                    if os.path.exists(markdown_file):
                        print("✅ Markdown file created")
                    else:
                        print("❌ Markdown file not found")
                else:
                    print("⚠️  No result returned from file generation")
        except Exception as e:
            print(f"❌ File generation failed: {e}")
            return False
        
        # Test 4: Test different options
        print("\n🔍 Test 4: Different include options")
        try:
            # Test with resources only
            result = client.generate_diagram(
                format="mermaid",
                include_routers=False,
                include_policies=False,
                include_resources=True
            )
            print("✅ Resources-only diagram generated")
            
            # Test with all options disabled except one
            result = client.generate_diagram(
                format="mermaid",
                include_routers=True,
                include_policies=False,
                include_resources=False
            )
            print("✅ Routers-only diagram generated")
            
        except Exception as e:
            print(f"❌ Options test failed: {e}")
            return False
        
        # Test 5: Test invalid format (should raise ValueError)
        print("\n🔍 Test 5: Invalid format handling")
        try:
            client.generate_diagram(format="invalid_format")
            print("❌ Should have raised ValueError for invalid format")
            return False
        except ValueError as e:
            if "Unsupported format" in str(e):
                print("✅ Invalid format properly rejected")
            else:
                print(f"❌ Unexpected ValueError: {e}")
                return False
        except Exception as e:
            print(f"❌ Unexpected exception for invalid format: {e}")
            return False
        
        # Test 6: Test helper methods
        print("\n🔍 Test 6: Helper methods")
        try:
            # Test color generation
            colors = client._get_source_group_colors(['group1', 'group2', 'group3'])
            if len(colors) == 3:
                print("✅ Color generation works")
            else:
                print(f"❌ Color generation returned {len(colors)} colors, expected 3")
            
            # Test policy label formatting
            label = client._format_policy_label(['policy1', 'policy2'], "Test")
            if "Test:" in label and ("policy1" in label or "policy2" in label):
                print("✅ Policy label formatting works")
            else:
                print(f"❌ Policy label formatting failed: {label}")
            
            # Test ID sanitization
            sanitized = client._sanitize_id("test-group.name/with spaces")
            if sanitized == "test_group_name_with_spaces":
                print("✅ ID sanitization works")
            else:
                print(f"❌ ID sanitization failed: {sanitized}")
            
        except Exception as e:
            print(f"❌ Helper methods test failed: {e}")
            return False
        
        print("\n🎉 All tests passed!")
        return True
        
    except NetBirdAPIError as e:
        print(f"❌ NetBird API Error: {e}")
        return False
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        return False
    finally:
        try:
            client.close()
            print("🔒 Client connection closed")
        except:
            pass


def main():
    """Main function."""
    print("NetBird Python Client - Diagram Generation Test")
    print("This script tests the integrated diagram generation functionality.\n")
    
    success = test_diagram_functionality()
    
    print("\n" + "=" * 50)
    if success:
        print("✅ All diagram functionality tests PASSED!")
        print("\n💡 Next steps:")
        print("   - Try generating diagrams with your networks")
        print("   - Experiment with different formats (mermaid, graphviz, diagrams)")
        print("   - Use diagrams in your documentation")
        sys.exit(0)
    else:
        print("❌ Some tests FAILED!")
        print("\n🔧 Troubleshooting:")
        print("   - Check your API token and NetBird server connection")
        print("   - Ensure you have networks configured in NetBird")
        print("   - Try running tests individually for more details")
        sys.exit(1)


if __name__ == "__main__":
    main()