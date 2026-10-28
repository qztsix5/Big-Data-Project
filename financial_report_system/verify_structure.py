#!/usr/bin/env python3
"""
Simple verification script that checks project structure without requiring dependencies.
"""
import os
from pathlib import Path


def check_file_exists(filepath, description):
    """Check if a file exists and print result."""
    exists = Path(filepath).exists()
    status = "✓" if exists else "✗"
    print(f"{status} {description}: {filepath}")
    return exists


def check_directory_exists(dirpath, description):
    """Check if a directory exists and print result."""
    exists = Path(dirpath).is_dir()
    status = "✓" if exists else "✗"
    print(f"{status} {description}: {dirpath}")
    return exists


def main():
    """Main verification function."""
    print("=" * 80)
    print("Financial Report Analysis System - Structure Verification")
    print("=" * 80)
    print()
    
    checks_passed = 0
    total_checks = 0
    
    # Check core files
    print("Core Files:")
    print("-" * 80)
    total_checks += 1
    checks_passed += check_file_exists("main.py", "Main application")
    total_checks += 1
    checks_passed += check_file_exists("requirements.txt", "Requirements file")
    total_checks += 1
    checks_passed += check_file_exists("README.md", "README")
    total_checks += 1
    checks_passed += check_file_exists(".env.example", "Environment template")
    total_checks += 1
    checks_passed += check_file_exists("test_system.py", "System test")
    print()
    
    # Check configuration
    print("Configuration:")
    print("-" * 80)
    total_checks += 1
    checks_passed += check_file_exists("config/config.yaml", "System configuration")
    print()
    
    # Check source modules
    print("Source Modules:")
    print("-" * 80)
    total_checks += 1
    checks_passed += check_file_exists("src/agents/financial_agent.py", "Financial Agent")
    total_checks += 1
    checks_passed += check_file_exists("src/data_processing/pdf_parser.py", "PDF Parser")
    total_checks += 1
    checks_passed += check_file_exists("src/data_processing/excel_parser.py", "Excel Parser")
    total_checks += 1
    checks_passed += check_file_exists("src/data_processing/web_scraper.py", "Web Scraper")
    total_checks += 1
    checks_passed += check_file_exists("src/data_processing/data_storage.py", "Data Storage")
    total_checks += 1
    checks_passed += check_file_exists("src/visualization/chart_generator.py", "Chart Generator")
    total_checks += 1
    checks_passed += check_file_exists("src/utils/config_loader.py", "Config Loader")
    total_checks += 1
    checks_passed += check_file_exists("src/utils/logger.py", "Logger")
    total_checks += 1
    checks_passed += check_file_exists("src/utils/stats_tracker.py", "Statistics Tracker")
    print()
    
    # Check examples
    print("Examples:")
    print("-" * 80)
    total_checks += 1
    checks_passed += check_file_exists("examples/example1_basic_query.py", "Example 1: Basic Query")
    total_checks += 1
    checks_passed += check_file_exists("examples/example2_advanced_analysis.py", "Example 2: Advanced Analysis")
    total_checks += 1
    checks_passed += check_file_exists("examples/example3_multi_turn.py", "Example 3: Multi-turn")
    total_checks += 1
    checks_passed += check_file_exists("examples/example4_complete_workflow.py", "Example 4: Complete Workflow")
    print()
    
    # Check documentation
    print("Documentation:")
    print("-" * 80)
    total_checks += 1
    checks_passed += check_file_exists("docs/SETUP.md", "Setup Guide")
    total_checks += 1
    checks_passed += check_file_exists("docs/REPORT.md", "Experimental Report")
    total_checks += 1
    checks_passed += check_file_exists("docs/QUICKSTART.md", "Quick Start Guide")
    print()
    
    # Check sample data
    print("Sample Data:")
    print("-" * 80)
    total_checks += 1
    checks_passed += check_file_exists("data/sample/generate_sample_data.py", "Sample Data Generator")
    total_checks += 1
    checks_passed += check_file_exists("data/sample/sample_financial_data.json", "Sample Financial Data")
    print()
    
    # Check directories
    print("Directory Structure:")
    print("-" * 80)
    total_checks += 1
    checks_passed += check_directory_exists("src", "Source directory")
    total_checks += 1
    checks_passed += check_directory_exists("src/agents", "Agents directory")
    total_checks += 1
    checks_passed += check_directory_exists("src/data_processing", "Data Processing directory")
    total_checks += 1
    checks_passed += check_directory_exists("src/visualization", "Visualization directory")
    total_checks += 1
    checks_passed += check_directory_exists("src/utils", "Utils directory")
    total_checks += 1
    checks_passed += check_directory_exists("examples", "Examples directory")
    total_checks += 1
    checks_passed += check_directory_exists("docs", "Docs directory")
    total_checks += 1
    checks_passed += check_directory_exists("data", "Data directory")
    total_checks += 1
    checks_passed += check_directory_exists("config", "Config directory")
    print()
    
    # Summary
    print("=" * 80)
    print(f"Verification Summary: {checks_passed}/{total_checks} checks passed")
    print("=" * 80)
    print()
    
    if checks_passed == total_checks:
        print("✓ All structure checks passed!")
        print()
        print("Next steps:")
        print("1. Install dependencies: pip install -r requirements.txt")
        print("2. Configure API key: cp .env.example .env && edit .env")
        print("3. Run examples: python examples/example4_complete_workflow.py")
        return 0
    else:
        print(f"⚠ {total_checks - checks_passed} checks failed")
        print("Please ensure all files are present")
        return 1


if __name__ == "__main__":
    exit(main())
