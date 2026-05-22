from setuptools import find_packages, setup


setup(
    name="graphmemshield",
    version="0.1.0",
    description="Auditing cross-session privacy leakage in dynamic KG-backed graph-backed application memory",
    author="GraphMemShield Research Team",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    python_requires=">=3.10",
    extras_require={
        "dev": ["pytest>=8.0.0"],
        "frameworks": ["langgraph>=1.2.0", "mem0ai>=2.0.0"],
        "attacks": ["scikit-learn>=1.8.0", "numpy>=2.0.0"],
        "llm": ["openai>=2.0.0"],
    },
)
