from setuptools import find_packages, setup


setup(
    name="django_prose",
    version="0.1.1",
    description=(
        "Elegant prose authoring for Django"
    ),
    url="https://github.com/sourcelair/django-prose",
    author="Paris Kasidiaris",
    author_email="accounts@sourcelair.com",
    license="MIT",
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "Topic :: Software Development",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
    ],
    keywords="prose development rich text",
    packages=find_packages(),
    include_package_data=True,
)
