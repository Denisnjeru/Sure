# from django.core.management import BaseCommand
#
#
# class Command(BaseCommand):
#     help = "seed database for testing and development."
#
#     def add_arguments(self, parser):
#         parser.add_argument("--mode", type=str, help="Mode")
#
#     def handle(self, *args, **options):
#         self.stdout.write("seeding data...")
#         run_seed(self, options["mode"])
#         self.stdout.write("done.")
#
#
# def clear_data():
#     """Deletes all the table data"""
#     print("Delete all data instances")
#
#     # model object to be deleted
#     q_models = [
#         BuyerPrivilege,
#         QedPrivilege,
#         QedRole,
#         BuyerRole,
#         CategoryGroup,
#         SourcingActivity,
#         Site,
#         Company,
#         Supplier,
#     ]
#
#     for model in q_models:
#         print("Deleted all {}".format(model))
#         model.objects.all().delete()
#
#
# def create_privileges():
#     """Creates qed and buyer privileges as requirement specifications"""
#     print("Creating privileges")
#
#     # privileges and their descriptions
#     qed_privileges = {
#         "User Management": "Ability to add, edit, activate, deactivate users",
#         "Criteria management": "Ability to create a job criteria (Sections, subsections and question items)",
#         "Category management": "Ability to create, edit and manage job categories including closing extensions",
#         "View Reports": "Ability to view system reports",
#         "Participant communication": "Ability to send participants a list of other participants at close of job",
#         "Job management": "Ability to create, edit, cancel a job.",
#         "Document Management": "Ability to create and edit contracts, award letters, regret letters and other system documents.",
#         "Generate Reports": "Ability to generate various system reports",
#     }
#
#     buyer_privileges = {
#         "Managing users": "Ability to add and edit users",
#         "Job management": "Ability to create a job criteria (Sections, subsections and question items)",
#         "Reports": "Ability to view reports",
#         "Categories managements": "Ability to create and edit categories",
#         "Participant communications": "Ability to send participants a list of other participants at close of job",
#         "Profile Management": "Ability to update company information.",
#         "Supplier information": "Ability to access supplier files and information",
#         "Supplier management": "Ability to blacklist whitelist suppliers",
#         "Document Management": "Ability to create and edit contracts, award letters, regret letters and other system documents.",
#         "Company Details": "Ability to edit and update company profile information.",
#     }
#     for privilege, description in qed_privileges.items():
#         QedPrivilege.objects.update_or_create(title=privilege, description=description)
#         print("QED: {} created".format(privilege))
#
#     for privilege, description in buyer_privileges.items():
#         BuyerPrivilege.objects.update_or_create(
#             title=privilege, description=description
#         )
#         print("Buyer: {} created".format(privilege))
#     return "Done"
#
#
# def create_roles():
#     """ Creates QED and Buyer roles as requirement specifications"""
#     print("Creating Roles")
#
#     # Roles and their descriptions
#     qed_roles = {
#         "Administrator": "Performs the administrative functions in the system as assigned in privileges",
#         "Staff": "Performs supportive functions in the system as assigned in privileges",
#     }
#
#     for role, description in qed_roles.items():
#         QedRole.objects.update_or_create(name=role, description=description)
#         print("QED: {} created".format(role))
#
#     return "Done"
#
#
# def create_category_groups():
#     """ Creates the category groups as specifications"""
#     print("Creating Category Groups")
#
#     category_groups = {"Works": "W", "Goods": "G", "Services": "S"}
#     for name, code in category_groups.items():
#         CategoryGroup.objects.update_or_create(name=name, code=code)
#         print("Group {} created".format(name))
#     return "Done"
#
#
# def create_qed_admin():
#     """ Creates the first qed admin for the system"""
#     print("Creating A Qed Admin")
#
#     admin_username = "eprocure@qedsolutions.co.ke"
#     qed_admin_password = "SupAdm@2019"
#
#     # check if the default admin has been created, delete them
#     qed = Qed.objects.filter(username=admin_username)
#     if len(qed) > 0:
#         qed.first().delete()
#
#     admin_data = {
#         "username": admin_username,
#         "first_name": "Sample Admin",
#         "email": admin_username,
#         "password1": qed_admin_password,
#         "password2": qed_admin_password,
#     }
#
#     form = QedAdminForm(admin_data)
#
#     if form.is_valid():
#         user = form.save(commit=False)
#         user.is_active = True
#         user.is_staff = True
#         user.email = form.cleaned_data.get("username")
#         user.set_password(qed_admin_password)
#         user.save()
#         qed = Qed.objects.get(user_ptr_id=user.id)
#         admin_role = QedRole.objects.filter(name="Administrator")
#         if len(admin_role) > 0:
#             admin_role = admin_role.first()
#         qed.qed_role = admin_role
#         qed.save()
#         print(
#             "Admin created: username {} password {}".format(
#                 user.username, qed_admin_password
#             )
#         )
#         print("Privilege to manage users granted to administrator")
#
#         # assign user management privilege to admin role for starters
#         qed_user_management_privilege = QedPrivilege.objects.filter(
#             title="User Management"
#         )
#         if len(qed_user_management_privilege) > 0:
#             qed_user_management_privilege = qed_user_management_privilege.first()
#
#             QedRolePrivilege.objects.get_or_create(
#                 qed_role=admin_role, qed_privilege=qed_user_management_privilege
#             )
#
#         return "Done"
#     else:
#         print(form)
#         print("Could not create admin. Please review seeder")
#
#
# def create_sites():
#     """
#     Creates sites to be used by pesapal
#     :return:
#     """
#
#     print("Creating sites")
#
#     sites = {
#         "staging": "staging.eprocure.co.ke",
#         "localhost": "localhost:8000",
#         "live": "e.tendersure.co.ke",
#     }
#     i = 1
#     for name, domain in sites.items():
#         Site.objects.update_or_create(name=name, domain=domain, id=i)
#         i += 1
#         print("Site {} created".format(name))
#     return "Done"
#
#
# def create_currencies():
#     """
#     Creates Currencies to be used on category bid charge dropdown.
#     :return:
#     """
#     print("Creating sites")
#
#     currencies = {"KES": "Kenyan Shillings", "USD": "US Dollars", "EUR": "Euros"}
#     i = 1
#     for initial, name in currencies.items():
#         Currency.objects.update_or_create(
#             initials=initial,
#             name=name,
#         )
#         i += 1
#     return "Done"
#
#
# def create_countries():
#     """
#     Creates coutries objects
#     :return:
#     """
#     print("Creating Countries")
#     countries = [
#         "Afghanistan",
#         "Albania",
#         "Algeria",
#         "Andorra",
#         "Angola",
#         "Antigua and Barbuda",
#         "Argentina",
#         "Armenia",
#         "Australia",
#         "Austria",
#         "Azerbaijan",
#         "Bahamas",
#         "Bahrain",
#         "Bangladesh",
#         "Barbados",
#         "Belarus",
#         "Belgium",
#         "Belize",
#         "Benin",
#         "Bhutan",
#         "Bolivia",
#         "Bosnia and Herzegovina",
#         "Botswana",
#         "Brazil",
#         "Brunei",
#         "Bulgaria",
#         "Burkina Faso",
#         "Burundi",
#         "Cabo Verde",
#         "Cambodia",
#         "Cameroon",
#         "Canada",
#         "Central African Republic (CAR)",
#         "Chad",
#         "Chile",
#         "China",
#         "Colombia",
#         "Comoros",
#         "Democratic Republic of the Congo",
#         "Republic of the Congo",
#         "Costa Rica",
#         "Cote d'Ivoire",
#         "Croatia",
#         "Cuba",
#         "Cyprus",
#         "Czech Republic",
#         "Denmark",
#         "Djibouti",
#         "Dominica",
#         "Dominican Republic",
#         "Ecuador",
#         "Egypt",
#         "El Salvador",
#         "Equatorial Guinea",
#         "Eritrea",
#         "Estonia",
#         "Eswatini (formerly Swaziland)",
#         "Ethiopia",
#         "Fiji",
#         "Finland",
#         "France",
#         "Gabon",
#         "Gambia",
#         "Georgia",
#         "Germany",
#         "Ghana",
#         "Greece",
#         "Grenada",
#         "Guatemala",
#         "Guinea",
#         "Guinea-Bissau",
#         "Guyana",
#         "Haiti",
#         "Honduras",
#         "Hungary",
#         "Iceland",
#         "India",
#         "Indonesia",
#         "Iran",
#         "Iraq",
#         "Ireland",
#         "Israel",
#         "Italy",
#         "Jamaica",
#         "Japan",
#         "Jordan",
#         "Kazakhstan",
#         "Kenya",
#         "Kiribati",
#         "Kosovo",
#         "Kuwait",
#         "Kyrgyzstan",
#         "Laos",
#         "Latvia",
#         "Lebanon",
#         "Lesotho",
#         "Liberia",
#         "Libya",
#         "Liechtenstein",
#         "Lithuania",
#         "Luxembourg",
#         "Macedonia (FYROM)",
#         "Madagascar",
#         "Malawi",
#         "Malaysia",
#         "Maldives",
#         "Mali",
#         "Malta",
#         "Marshall Islands",
#         "Mauritania",
#         "Mauritius",
#         "Mexico",
#         "Micronesia",
#         "Moldova",
#         "Monaco",
#         "Mongolia",
#         "Montenegro",
#         "Morocco",
#         "Mozambique",
#         "Myanmar (formerly Burma)",
#         "Namibia",
#         "Nauru",
#         "Nepal",
#         "Netherlands",
#         "New Zealand",
#         "Nicaragua",
#         "Niger",
#         "Nigeria",
#         "North Korea",
#         "Norway",
#         "Oman",
#         "Pakistan",
#         "Palau",
#         "Palestine",
#         "Panama",
#         "Papua New Guinea",
#         "Paraguay",
#         "Peru",
#         "Philippines",
#         "Poland",
#         "Portugal",
#         "Qatar",
#         "Romania",
#         "Russia",
#         "Rwanda",
#         "Saint Kitts and Nevis",
#         "Saint Lucia",
#         "Saint Vincent and the Grenadines",
#         "Samoa",
#         "San Marino",
#         "Sao Tome and Principe",
#         "Saudi Arabia",
#         "Senegal",
#         "Serbia",
#         "Seychelles",
#         "Sierra Leone",
#         "Singapore",
#         "Slovakia",
#         "Slovenia",
#         "Solomon Islands",
#         "Somalia",
#         "South Africa",
#         "South Korea",
#         "South Sudan",
#         "Spain",
#         "Sri Lanka",
#         "Sudan",
#         "Suriname",
#         "Swaziland (renamed to Eswatini)",
#         "Sweden",
#         "Switzerland",
#         "Syria",
#         "Taiwan",
#         "Tajikistan",
#         "Tanzania",
#         "Thailand",
#         "Timor-Leste",
#         "Togo",
#         "Tonga",
#         "Trinidad and Tobago",
#         "Tunisia",
#         "Turkey",
#         "Turkmenistan",
#         "Tuvalu",
#         "Uganda",
#         "Ukraine",
#         "United Arab Emirates (UAE)",
#         "United Kingdom (UK)",
#         "United States of America (USA)",
#         "Uruguay",
#         "Uzbekistan",
#         "Vanuatu",
#         "Vatican City (Holy See)",
#         "Venezuela",
#         "Vietnam",
#         "Yemen",
#         "Zambia",
#         "Zimbabwe",
#     ]
#     for country in countries:
#         print(country)
#         Country.objects.update_or_create(name=country)
#     return "Done"
#
#
# def create_Locations():
#     """
#     Creates Locations objects
#     :return:
#     """
#     print("Creating Locations")
#     locationas = [
#         "Mombasa",
#         "Kwale",
#         "Kilifi",
#         "Tana River",
#         "Lamu",
#         "Taita-Taveta",
#         "Garissa",
#         "Wajir",
#         "Mandera",
#         "Marsabit",
#         "Isiolo",
#         "Meru",
#         "Tharaka-Nithi",
#         "Embu",
#         "Kitui",
#         "Machakos",
#         "Makueni",
#         "Nyandarua",
#         "Nyeri",
#         "Kirinyaga",
#         "Muranga",
#         "Kiambu",
#         "Turkana",
#         "West Pokot",
#         "Samburu",
#         "Trans-Nzoia",
#         "Uasin Gishu",
#         "Elgeyo-Marakwet",
#         "Nandi",
#         "Baringo",
#         "Laikipia",
#         "Nakuru",
#         "Narok",
#         "Kajiado",
#         "Kericho",
#         "Bomet",
#         "Kakamega",
#         "Vihiga",
#         "Bungoma",
#         "Busia",
#         "Siaya",
#         "Kisumu",
#         "Homa Bay",
#         "Migori",
#         "Kisii",
#         "Nyamira",
#         "Nairobi",
#     ]
#
#     k = Country.objects.filter(id=88).first()
#     for locationa in locationas:
#         print(locationa)
#         Location.objects.update_or_create(Country=k, name=locationa)
#     return "Done"
#
#
# def create_cameroon_locations():
#     """
#     Create cameroon locations
#     """
#     print("Creating Locations Cameroon")
#     locations = [
#         "DOUALA",
#         "MBANGA",
#         "NJOMBE",
#         "LOUM",
#         "MANJO",
#         "NKONGSAMBA",
#         "MELONG",
#         "POUMA",
#         "EDEA",
#         "YABASSI",
#         "ZOETELE ",
#         "SANGMELIMA",
#         "EBOME",
#         "KRIBI",
#         "YOLA",
#         "KYE-OSSI",
#         "AMBAM",
#         "DJOUM",
#         "LOLODORF",
#         "NIETE HEVECAM",
#         "YAOUNDE",
#         "AKONOLINGA",
#         "ESSEKA",
#         "ENDOUM",
#         "OKOLA",
#         "MFOU",
#         "SOA",
#         "BAFOUSSAM",
#         "DSCHANG",
#         "FOUMBOT",
#         "FOUMBAN",
#         "BABADJOU",
#         "LEPI",
#         "BOUDA",
#         "MONATELE",
#         "BUEA" "LIMBE",
#         "BERTOUA",
#         "NGAOUNDERE",
#         "GAROUA",
#         "MAROUA",
#         "BAMENDA",
#     ]
#
#     cameroon = Country.objects.filter(id=31).first()
#     for location in locations:
#         print(location)
#         Location.objects.update_or_create(Country=cameroon, name=location.lower())
#     return "Done"
#
#
# def create_uganda_locations():
#     """
#     Create Uganda locations
#     """
#     print("Creating Locations Uganda")
#     locations = [
#         "Kampala",
#         "Nansana",
#         "Kira",
#         "Ssabagabo",
#         "Mbarara",
#         "Mukono",
#         "Njeru",
#         "Gulu",
#         "Lugazi",
#         "Masaka",
#         "Kasese",
#         "Hoima",
#         "Lira",
#         "Mityana",
#         "Mubende",
#         "Masindi",
#         "Mbale",
#         "Jinja",
#         "Entebbe",
#         "Kitgum",
#     ]
#
#     uganda = Country.objects.filter(id=185).first()
#     for location in locations:
#         print(location)
#         Location.objects.update_or_create(Country=uganda, name=location.lower())
#     return "Done"
#
#
# def create_tanzania_locations():
#     """
#     Create Tanzania locations
#     """
#     print("Creating Locations Tanzania")
#     locations = [
#         "Arusha",
#         "Dar es Salaam",
#         "Dodoma",
#         "Geita",
#         "Iringa",
#         "Kagera",
#         "Katavi",
#         "Kigoma",
#         "Kilimanjaro",
#         "Lindi",
#         "Manyara",
#         "Mara",
#         "Mbeya",
#         "Minji Magharibi",
#         "Mtwara",
#         "Morogoro",
#         "Mwanza",
#         "Njombe",
#         "Pemba North",
#         "Pemba South",
#         "Rukwa",
#         "Ruvuma",
#         "Shinyanga",
#         "Simiyu",
#         "Singida",
#         "Songwe",
#         "Tabora",
#         "Ugunja North",
#         "Ugunja South",
#     ]
#
#     tanzania = Country.objects.filter(id=175).first()
#     for location in locations:
#         print(location)
#         Location.objects.update_or_create(Country=tanzania, name=location.lower())
#     return "Done"
#
#
# def create_mozambique_locations():
#     """
#     Create Mozambique locations
#     """
#     print("Creating Locations Mozambique")
#     locations = [
#         "Maputo",
#         "Bilene",
#         "Chibuto",
#         "Chokwe",
#         "Chongoene",
#         "Cidade De Xai-Xai",
#         "Guija",
#         "Limpopo",
#         "Mandlakaze",
#         "Mapai",
#         "Mabalane",
#         "Massingir",
#         "Funhalouro",
#         "Jangamo",
#         "Guvuro",
#         "Homoine",
#         "Inhambane",
#         "Inharrime",
#         "Inhassoro",
#         "Mabote",
#         "Massinga",
#         "Maxixe",
#         "Morrumbene",
#         "Vilanculos",
#         "Zavala",
#         "Panda",
#     ]
#     mozambique = Country.objects.filter(id=119).first()
#     for location in locations:
#         print(location)
#         Location.objects.update_or_create(Country=mozambique, name=location)
#     return "Done"
#
#
# def create_settings():
#     """ Seeds all settings in the system"""
#     print("Performing setup.")
#
#     settings = {
#         "Terms": "Terms of usage will go <b>here</b>",
#     }
#     for description, value in settings.items():
#         qed_admin = Qed.objects.filter(username="eprocure@qedsolutions.co.ke").first()
#         name = description.replace(" ", "_").upper()
#         previous_setting = Setting.objects.filter(name=name).first()
#         if qed_admin is not None:
#             if previous_setting is not None:
#                 value = previous_setting.value
#                 description = previous_setting.description
#             Setting.objects.update_or_create(
#                 defaults={
#                     "description": description,
#                     "value": value,
#                     "updated_by": qed_admin,
#                 },
#                 name=name,
#             )
#             print("Setting {} created".format(description))
#     return "Done"
#
#
# def run_seed(self, mode):
#     """Seed database based on mode
#
#     :param mode: refresh / clear
#     :return:
#     """
#     mode_clear = "fresh"
#     # Clear data from tables
#     if mode == mode_clear:
#         clear_data()
#
#     # Creating NEW DATA
#     # create_countries()
#     # create_Locations()
#     # create_currencies()
#     # create_privileges()
#     # create_roles()
#     # create_sourcing_activities()
#     # create_category_groups()
#     # create_qed_admin()
#     # create_sites()
#     # create_settings()
#     # create_cameroon_locations()
#     # create_tanzania_locations()
#     # create_uganda_locations()
#     # create_mozambique_locations()
#     pass
