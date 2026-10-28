"""
Sample data generator for demonstration purposes.
"""
import json
from pathlib import Path


def generate_sample_data():
    """Generate sample financial data for demonstration."""
    
    sample_data = {
        "阿里巴巴": {
            "2020": {
                "revenue": "724,523",
                "net_profit": "54,874",
                "total_assets": "1,432,456",
                "total_liabilities": "876,234",
                "gross_margin": "35.8",
                "roe": "8.2",
                "operating_cash_flow": "125,678",
                "asset_liability_ratio": "61.2"
            },
            "2021": {
                "revenue": "817,267",
                "net_profit": "62,628",
                "total_assets": "1,543,678",
                "total_liabilities": "923,456",
                "gross_margin": "36.5",
                "roe": "8.5",
                "operating_cash_flow": "142,345",
                "asset_liability_ratio": "59.8"
            },
            "2022": {
                "revenue": "868,687",
                "net_profit": "68,574",
                "total_assets": "1,612,345",
                "total_liabilities": "967,890",
                "gross_margin": "37.1",
                "roe": "8.7",
                "operating_cash_flow": "156,789",
                "asset_liability_ratio": "60.0"
            },
            "2023": {
                "revenue": "868,687",
                "net_profit": "71,337",
                "total_assets": "1,594,023",
                "total_liabilities": "945,678",
                "gross_margin": "37.2",
                "roe": "8.5",
                "operating_cash_flow": "168,234",
                "asset_liability_ratio": "59.3"
            },
            "2024": {
                "revenue": "941,168",
                "net_profit": "80,234",
                "total_assets": "1,687,456",
                "total_liabilities": "987,654",
                "gross_margin": "38.5",
                "roe": "9.1",
                "operating_cash_flow": "189,567",
                "asset_liability_ratio": "58.5"
            }
        },
        "腾讯": {
            "2020": {
                "revenue": "482,064",
                "net_profit": "159,847",
                "total_assets": "987,654",
                "total_liabilities": "456,789",
                "gross_margin": "44.8",
                "roe": "24.1",
                "operating_cash_flow": "187,234",
                "asset_liability_ratio": "46.2"
            },
            "2021": {
                "revenue": "560,118",
                "net_profit": "224,823",
                "total_assets": "1,098,765",
                "total_liabilities": "498,765",
                "gross_margin": "45.2",
                "roe": "26.3",
                "operating_cash_flow": "213,456",
                "asset_liability_ratio": "45.4"
            },
            "2022": {
                "revenue": "554,552",
                "net_profit": "186,880",
                "total_assets": "1,134,567",
                "total_liabilities": "512,345",
                "gross_margin": "43.5",
                "roe": "21.8",
                "operating_cash_flow": "198,765",
                "asset_liability_ratio": "45.1"
            },
            "2023": {
                "revenue": "609,020",
                "net_profit": "232,436",
                "total_assets": "1,245,678",
                "total_liabilities": "534,567",
                "gross_margin": "46.1",
                "roe": "24.9",
                "operating_cash_flow": "234,567",
                "asset_liability_ratio": "42.9"
            },
            "2024": {
                "revenue": "667,723",
                "net_profit": "297,561",
                "total_assets": "1,356,789",
                "total_liabilities": "567,890",
                "gross_margin": "47.8",
                "roe": "28.2",
                "operating_cash_flow": "278,901",
                "asset_liability_ratio": "41.8"
            }
        },
        "比亚迪": {
            "2020": {
                "revenue": "133,082",
                "net_profit": "4,242",
                "total_assets": "234,567",
                "total_liabilities": "167,890",
                "gross_margin": "16.2",
                "roe": "6.1",
                "operating_cash_flow": "18,765",
                "asset_liability_ratio": "71.6",
                "new_energy_vehicle_sales": "179,054"
            },
            "2021": {
                "revenue": "216,142",
                "net_profit": "3,045",
                "total_assets": "289,456",
                "total_liabilities": "198,765",
                "gross_margin": "17.1",
                "roe": "4.2",
                "operating_cash_flow": "24,567",
                "asset_liability_ratio": "68.7",
                "new_energy_vehicle_sales": "603,783"
            },
            "2022": {
                "revenue": "424,067",
                "net_profit": "16,622",
                "total_assets": "387,654",
                "total_liabilities": "245,678",
                "gross_margin": "18.9",
                "roe": "11.2",
                "operating_cash_flow": "45,678",
                "asset_liability_ratio": "63.4",
                "new_energy_vehicle_sales": "1,863,494"
            },
            "2023": {
                "revenue": "602,316",
                "net_profit": "30,041",
                "total_assets": "476,543",
                "total_liabilities": "289,765",
                "gross_margin": "21.9",
                "roe": "17.8",
                "operating_cash_flow": "67,890",
                "asset_liability_ratio": "60.8",
                "new_energy_vehicle_sales": "3,024,417"
            },
            "2024": {
                "revenue": "745,523",
                "net_profit": "43,567",
                "total_assets": "567,890",
                "total_liabilities": "334,567",
                "gross_margin": "23.2",
                "roe": "21.3",
                "operating_cash_flow": "89,123",
                "asset_liability_ratio": "58.9",
                "new_energy_vehicle_sales": "4,271,589"
            }
        }
    }
    
    return sample_data


def save_sample_data():
    """Save sample data to JSON file."""
    data = generate_sample_data()
    
    # Create data directory
    data_dir = Path("data/sample")
    data_dir.mkdir(parents=True, exist_ok=True)
    
    # Save to JSON
    output_file = data_dir / "sample_financial_data.json"
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    
    print(f"Sample data saved to: {output_file}")
    print(f"Companies: {', '.join(data.keys())}")
    print(f"Years: 2020-2024")
    print(f"Metrics per company per year: 8-9")


if __name__ == "__main__":
    save_sample_data()
