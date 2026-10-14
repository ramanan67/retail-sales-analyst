from setuptools import setup, find_packages

setup(
    name="retail-sales-analytics",
    version="1.0.0",
    package_dir={"": "src"},
    packages=find_packages(where="src"),
    include_package_data=True,
    entry_points={
        "console_scripts": [
            "retail-sales=retail_sales_analytics.cli:main",
            "retail-analytics=retail_sales_analytics.cli:main",
        ],
    },
)
