from django.core.management.base import BaseCommand
from apps.buyer.models import BuyerPrivilege

from apps.common.models import Country, Location
from apps.qed.models import QedPrivilege


class Command(BaseCommand):
    def handle(self, *args, **options):
        self.stdout.write("running management command ..")
        create_countries()
        create_locations()
        self.stdout.write("job complete")


def create_countries():
    """
    Creates coutries objects
    :return:
    """
    print("Creating Countries")
    countries = [
        "Afghanistan",
        "Albania",
        "Algeria",
        "Andorra",
        "Angola",
        "Antigua and Barbuda",
        "Argentina",
        "Armenia",
        "Australia",
        "Austria",
        "Azerbaijan",
        "Bahamas",
        "Bahrain",
        "Bangladesh",
        "Barbados",
        "Belarus",
        "Belgium",
        "Belize",
        "Benin",
        "Bhutan",
        "Bolivia",
        "Bosnia and Herzegovina",
        "Botswana",
        "Brazil",
        "Brunei",
        "Bulgaria",
        "Burkina Faso",
        "Burundi",
        "Cabo Verde",
        "Cambodia",
        "Cameroon",
        "Canada",
        "Central African Republic (CAR)",
        "Chad",
        "Chile",
        "China",
        "Colombia",
        "Comoros",
        "Democratic Republic of the Congo",
        "Republic of the Congo",
        "Costa Rica",
        "Cote d'Ivoire",
        "Croatia",
        "Cuba",
        "Cyprus",
        "Czech Republic",
        "Denmark",
        "Djibouti",
        "Dominica",
        "Dominican Republic",
        "Ecuador",
        "Egypt",
        "El Salvador",
        "Equatorial Guinea",
        "Eritrea",
        "Estonia",
        "Eswatini (formerly Swaziland)",
        "Ethiopia",
        "Fiji",
        "Finland",
        "France",
        "Gabon",
        "Gambia",
        "Georgia",
        "Germany",
        "Ghana",
        "Greece",
        "Grenada",
        "Guatemala",
        "Guinea",
        "Guinea-Bissau",
        "Guyana",
        "Haiti",
        "Honduras",
        "Hungary",
        "Iceland",
        "India",
        "Indonesia",
        "Iran",
        "Iraq",
        "Ireland",
        "Israel",
        "Italy",
        "Jamaica",
        "Japan",
        "Jordan",
        "Kazakhstan",
        "Kenya",
        "Kiribati",
        "Kosovo",
        "Kuwait",
        "Kyrgyzstan",
        "Laos",
        "Latvia",
        "Lebanon",
        "Lesotho",
        "Liberia",
        "Libya",
        "Liechtenstein",
        "Lithuania",
        "Luxembourg",
        "Macedonia (FYROM)",
        "Madagascar",
        "Malawi",
        "Malaysia",
        "Maldives",
        "Mali",
        "Malta",
        "Marshall Islands",
        "Mauritania",
        "Mauritius",
        "Mexico",
        "Micronesia",
        "Moldova",
        "Monaco",
        "Mongolia",
        "Montenegro",
        "Morocco",
        "Mozambique",
        "Myanmar (formerly Burma)",
        "Namibia",
        "Nauru",
        "Nepal",
        "Netherlands",
        "New Zealand",
        "Nicaragua",
        "Niger",
        "Nigeria",
        "North Korea",
        "Norway",
        "Oman",
        "Pakistan",
        "Palau",
        "Palestine",
        "Panama",
        "Papua New Guinea",
        "Paraguay",
        "Peru",
        "Philippines",
        "Poland",
        "Portugal",
        "Qatar",
        "Romania",
        "Russia",
        "Rwanda",
        "Saint Kitts and Nevis",
        "Saint Lucia",
        "Saint Vincent and the Grenadines",
        "Samoa",
        "San Marino",
        "Sao Tome and Principe",
        "Saudi Arabia",
        "Senegal",
        "Serbia",
        "Seychelles",
        "Sierra Leone",
        "Singapore",
        "Slovakia",
        "Slovenia",
        "Solomon Islands",
        "Somalia",
        "South Africa",
        "South Korea",
        "South Sudan",
        "Spain",
        "Sri Lanka",
        "Sudan",
        "Suriname",
        "Swaziland (renamed to Eswatini)",
        "Sweden",
        "Switzerland",
        "Syria",
        "Taiwan",
        "Tajikistan",
        "Tanzania",
        "Thailand",
        "Timor-Leste",
        "Togo",
        "Tonga",
        "Trinidad and Tobago",
        "Tunisia",
        "Turkey",
        "Turkmenistan",
        "Tuvalu",
        "Uganda",
        "Ukraine",
        "United Arab Emirates (UAE)",
        "United Kingdom (UK)",
        "United States of America (USA)",
        "Uruguay",
        "Uzbekistan",
        "Vanuatu",
        "Vatican City (Holy See)",
        "Venezuela",
        "Vietnam",
        "Yemen",
        "Zambia",
        "Zimbabwe",
    ]
    if Country.objects.all().count() > 1:
        Country.objects.all().delete()
    for country in countries:
        print(country)
        Country.objects.update_or_create(name=country)
    return "Done"


def create_locations():
    """
    Creates Locations objects
    :return:
    """
    print("Creating Locations")
    locations = [
        "Mombasa",
        "Kwale",
        "Kilifi",
        "Tana River",
        "Lamu",
        "Taita-Taveta",
        "Garissa",
        "Wajir",
        "Mandera",
        "Marsabit",
        "Isiolo",
        "Meru",
        "Tharaka-Nithi",
        "Embu",
        "Kitui",
        "Machakos",
        "Makueni",
        "Nyandarua",
        "Nyeri",
        "Kirinyaga",
        "Muranga",
        "Kiambu",
        "Turkana",
        "West Pokot",
        "Samburu",
        "Trans-Nzoia",
        "Uasin Gishu",
        "Elgeyo-Marakwet",
        "Nandi",
        "Baringo",
        "Laikipia",
        "Nakuru",
        "Narok",
        "Kajiado",
        "Kericho",
        "Bomet",
        "Kakamega",
        "Vihiga",
        "Bungoma",
        "Busia",
        "Siaya",
        "Kisumu",
        "Homa Bay",
        "Migori",
        "Kisii",
        "Nyamira",
        "Nairobi",
    ]

    k = Country.objects.filter(id=88).first()
    for loc in locations:
        print(loc)
        Location.objects.update_or_create(country=k, name=loc)
    return "Done"

def create_privileges():
    """Creates qed and buyer privileges as requirement specifications"""
    print("Creating privileges")

    # privileges and their descriptions
    qed_privileges = {
        "User Management": "Ability to add, edit, activate, deactivate users",
        "Criteria management": "Ability to create a job criteria (Sections, subsections and question items)",
        "Category management": "Ability to create, edit and manage job categories including closing extensions",
        "View Reports": "Ability to view system reports",
        "Participant communication": "Ability to send participants a list of other participants at close of job",
        "Job management": "Ability to create, edit, cancel a job.",
        "Document Management": "Ability to create and edit contracts, award letters, regret letters and other system documents.",
        "Generate Reports": "Ability to generate various system reports",
    }

    buyer_privileges = {
        "Managing users": "Ability to add and edit users",
        "Job management": "Ability to create a job criteria (Sections, subsections and question items)",
        "Reports": "Ability to view reports",
        "Categories managements": "Ability to create and edit categories",
        "Participant communications": "Ability to send participants a list of other participants at close of job",
        "Profile Management": "Ability to update company information.",
        "Supplier information": "Ability to access supplier files and information",
        "Supplier management": "Ability to blacklist whitelist suppliers",
        "Document Management": "Ability to create and edit contracts, award letters, regret letters and other system documents.",
        "Company Details": "Ability to edit and update company profile information.",
    }
    for privilege, description in qed_privileges.items():
        QedPrivilege.objects.update_or_create(title=privilege, description=description)
        print("QED: {} created".format(privilege))

    for privilege, description in buyer_privileges.items():
        BuyerPrivilege.objects.update_or_create(
            title=privilege, description=description
        )
        print("Buyer: {} created".format(privilege))
    return "Done"
    
def run_seed():
    pass
