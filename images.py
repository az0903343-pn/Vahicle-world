"""
Real vehicle photos for the app (hotlinked from Wikimedia Commons - stable, free URLs).

- VEHICLE_IMAGES  : image URL per vehicle name (exact match with vehicles.csv)
- CATEGORY_IMAGES : fallback image per category (used when a vehicle has no photo)
- image_for()     : helper used by app.py and chatbot.py
"""
B = "https://upload.wikimedia.org/wikipedia/commons/thumb/"

# ---- shared URLs ----
Mehr = B + "7/70/Mehran_Model_2001_Right_Side_View_At_Lowari_Pass%2CChitral%2CKPK.jpg/640px-Mehran_Model_2001_Right_Side_View_At_Lowari_Pass%2CChitral%2CKPK.jpg"
CD70 = B + "4/4f/Honda_70_2025.jpg/960px-Honda_70_2025.jpg"
CG125 = B + "d/dc/%E3%83%9B%E3%83%B3%E3%83%80_CG125.jpg/960px-%E3%83%9B%E3%83%B3%E3%83%80_CG125.jpg"
YBR = B + "7/7f/Yamaha_YBR125_%28Fuel_Injection_-_EU_Spec%29.JPG/960px-Yamaha_YBR125_%28Fuel_Injection_-_EU_Spec%29.JPG"
Hiace = B + "8/80/2020_Toyota_HiAce_%28front%29.jpg/960px-2020_Toyota_HiAce_%28front%29.jpg"
Carry = B + "2/21/Suzuki_Carry_Truck_KC_4WD_DA16T.JPG/960px-Suzuki_Carry_Truck_KC_4WD_DA16T.JPG"
Civic22 = B + "b/b5/2022_Honda_Civic_Touring_in_Lunar_Silver_Metallic%2C_Front_Left%2C_05-10-2022.jpg/960px-2022_Honda_Civic_Touring_in_Lunar_Silver_Metallic%2C_Front_Left%2C_05-10-2022.jpg"
C172 = B + "a/ae/Cessna_172S_Skyhawk_SP%2C_Private_JP6817606.jpg/960px-Cessna_172S_Skyhawk_SP%2C_Private_JP6817606.jpg"
M2 = B + "0/0f/OO-FLN.JPG/960px-OO-FLN.JPG"
Rickshaw = B + "4/49/Bajaj_auto-rickshaw_in_Sri_Lanka.jpg/640px-Bajaj_auto-rickshaw_in_Sri_Lanka.jpg"
Motorboat = B + "d/d9/Motorboat_at_Kankaria_lake.JPG/640px-Motorboat_at_Kankaria_lake.JPG"
HD883 = B + "4/4f/Flickr_-_ronsaunders47_-_HARLEY-DAVIDSON_XR1200_SPORTSTER._2010..jpg/960px-Flickr_-_ronsaunders47_-_HARLEY-DAVIDSON_XR1200_SPORTSTER._2010..jpg"

CATEGORY_IMAGES = {
    "Generic Cycle": B + "5/58/Chase-ACT-Carbon-1.jpg/640px-Chase-ACT-Carbon-1.jpg",
    "Cycle": B + "9/96/Orbea_Occam_2020.jpg/640px-Orbea_Occam_2020.jpg",
    "Electric Bike": B + "b/b4/Electric_Wheels_in_Fort_Lauderdale%2C_Florida.jpg/640px-Electric_Wheels_in_Fort_Lauderdale%2C_Florida.jpg",
    "Scooter": B + "f/f3/Yamaha_Aerox_2011_.jpg/640px-Yamaha_Aerox_2011_.jpg",
    "Petrol Bike": B + "5/50/Istockphoto-114285168-612x612.jpg/640px-Istockphoto-114285168-612x612.jpg",
    "Heavy Bike": B + "1/1a/Yamaha_R1.jpg/640px-Yamaha_R1.jpg",
    "Rickshaw": Rickshaw,
    "Van": B + "1/1a/2018_Ford_Transit_Custom_300_Base_2.0_facelift.jpg/640px-2018_Ford_Transit_Custom_300_Base_2.0_facelift.jpg",
    "Car": B + "6/64/2005_Toyota_Corolla_%28ZZE122R_5Y%29_Ascent_sedan_01.jpg/640px-2005_Toyota_Corolla_%28ZZE122R_5Y%29_Ascent_sedan_01.jpg",
    "Bus/Truck": B + "8/83/2001_Ford_F-250_Super_Duty_XL_regular_cab_flatbed%2C_front_left%2C_05-17-2025.jpg/640px-2001_Ford_F-250_Super_Duty_XL_regular_cab_flatbed%2C_front_left%2C_05-17-2025.jpg",
    "Tractor": B + "8/85/Ford_8N.jpg/640px-Ford_8N.jpg",
    "Boat": Motorboat,
    "Helicopter": B + "7/70/VH-SUF_Taking_Off.jpg/640px-VH-SUF_Taking_Off.jpg",
    "Aircraft": C172,
    "Jet": M2,
}

VEHICLE_IMAGES = {
    # ---------------- cycles ----------------
    "Imported Road Racing Bike": B + "9/96/Orbea_Occam_2020.jpg/640px-Orbea_Occam_2020.jpg",
    "Giant ATX Mountain Bike": B + "9/96/Orbea_Occam_2020.jpg/640px-Orbea_Occam_2020.jpg",
    "Fat Bike 26 inch": B + "5/58/Chase-ACT-Carbon-1.jpg/640px-Chase-ACT-Carbon-1.jpg",
    "Trek Marlin 5 (imported)": B + "9/96/Orbea_Occam_2020.jpg/640px-Orbea_Occam_2020.jpg",
    # ---------------- electric ----------------
    "Electric Cycle (pedal assist)": B + "b/b4/Electric_Wheels_in_Fort_Lauderdale%2C_Florida.jpg/640px-Electric_Wheels_in_Fort_Lauderdale%2C_Florida.jpg",
    "Zongshen RX1 200cc": B + "b/bf/Zs200gs003.jpg/640px-Zs200gs003.jpg",
    # ---------------- scooters ----------------
    "Honda Activa 6G (imported)": B + "e/ec/Gold_Metallic_Honda_Activa.jpg/960px-Gold_Metallic_Honda_Activa.jpg",
    "Suzuki Access 125": B + "4/4d/BURGMAN650_K6.JPG/960px-BURGMAN650_K6.JPG",
    "Vespa 150 (imported)": B + "b/b8/PerthVespa.jpg/960px-PerthVespa.jpg",
    "Yamaha Zuma 125 (imported)": B + "0/0c/MBK_Booster%2C_yellow.jpg/960px-MBK_Booster%2C_yellow.jpg",
    # ---------------- petrol bikes ----------------
    "Honda CD 70": CD70,
    "Honda CD 70 Dream": CD70,
    "Honda CG 125": CG125,
    "Honda CG 125 Self Start": CG125,
    "Yamaha YBR 125": YBR,
    "Yamaha YBR 125G": YBR,
    "Honda CB 125F": B + "6/6d/Honda_CBF125_2009.jpg/960px-Honda_CBF125_2009.jpg",
    "Suzuki GSX 125": B + "5/5a/Suzuki_EN125_Thunder.jpg/960px-Suzuki_EN125_Thunder.jpg",
    # ---------------- heavy bikes ----------------
    "Honda CB 350 (imported)": B + "e/ec/Honda_350.jpg/960px-Honda_350.jpg",
    "KTM Duke 200 (imported)": B + "1/14/2020_Duke_200.jpg/960px-2020_Duke_200.jpg",
    "KTM Duke 390 (imported)": B + "8/8d/Ktm_duke_390.jpg/960px-Ktm_duke_390.jpg",
    "Kawasaki Ninja 400 (imported)": B + "8/8b/2026-06-27_Moscow_electric_vehicle_parade%2C_display_20_Kawasaki_Ninja.jpg/960px-2026-06-27_Moscow_electric_vehicle_parade%2C_display_20_Kawasaki_Ninja.jpg",
    "Honda CB 500F (imported)": B + "7/77/2023_Honda_CB500_Hornet.jpg/960px-2023_Honda_CB500_Hornet.jpg",
    "Kawasaki Z900 (imported)": B + "b/bc/Kawasaki_Z900%2C_green.jpg/960px-Kawasaki_Z900%2C_green.jpg",
    "Yamaha R1 (imported used)": B + "5/51/2015_Yamaha_YZF-R1_crop.JPG/960px-2015_Yamaha_YZF-R1_crop.JPG",
    "Honda CBR 650R (imported)": B + "f/ff/2023_Honda_CBR650R_E-Clutch.jpg/960px-2023_Honda_CBR650R_E-Clutch.jpg",
    "Harley-Davidson Iron 883 (imported used)": HD883,
    "Suzuki Hayabusa (imported used)": B + "d/de/SUZUKI_Hayabusa_2007TMS.jpg/960px-SUZUKI_Hayabusa_2007TMS.jpg",
    "BMW S 1000 RR (imported used)": B + "d/d5/BMW_S_1000_RR_-_BMW_M_1000_RR_50_Years_M_%2822121615413%29.jpg/960px-BMW_S_1000_RR_-_BMW_M_1000_RR_50_Years_M_%2822121615413%29.jpg",
    # ---------------- rickshaws ----------------
    "Auto Rickshaw (CNG)": Rickshaw,
    "Siwa Rickshaw (CNG)": Rickshaw,
    "Sazgar Auto Rickshaw (CNG)": Rickshaw,
    "Electric Passenger Rickshaw": Rickshaw,
    # ---------------- vans ----------------
    "Suzuki Bolan": Carry,
    "Suzuki Every (imported used)": B + "7/76/Suzuki_Every_DA17V_PA_Limited.jpg/960px-Suzuki_Every_DA17V_PA_Limited.jpg",
    "Toyota Hiace GL": Hiace,
    "Toyota Hiace Grand Cabin": Hiace,
    # ---------------- cars ----------------
    "Suzuki Mehran VXR (used)": Mehr,
    "Mitsubishi Ek Wagon (imported used)": B + "8/8c/Mitsubishi_eK_wagon_G_%285BA-B33W-LTCE%29_front.jpg/960px-Mitsubishi_eK_wagon_G_%285BA-B33W-LTCE%29_front.jpg",
    "Honda N Wgn (imported used)": B + "0/03/Honda_N-WGN_G_%28JH1%29_front.JPG/960px-Honda_N-WGN_G_%28JH1%29_front.JPG",
    "Suzuki Spacia (imported used)": B + "c/c3/Spacia-mk42s-4WD-with-foglamps.jpg/960px-Spacia-mk42s-4WD-with-foglamps.jpg",
    "Kia Picanto 1.0 AT": B + "8/8d/2018_Kia_Picanto_3_Automatic_1.2_Front.jpg/960px-2018_Kia_Picanto_3_Automatic_1.2_Front.jpg",
    "Suzuki Alto VXR": B + "5/55/1994-1997_Suzuki_Alto.jpg/960px-1994-1997_Suzuki_Alto.jpg",
    "Toyota Vitz (imported used)": B + "8/85/2017_Toyota_Yaris_L_5-door%2C_front_right%2C_08-25-2024.jpg/960px-2017_Toyota_Yaris_L_5-door%2C_front_right%2C_08-25-2024.jpg",
    "Suzuki Wagon R VXL": B + "3/35/1996_Suzuki_Wagon_R_RX_in_Radiant_Red_Mica%2C_front_left.jpg/960px-1996_Suzuki_Wagon_R_RX_in_Radiant_Red_Mica%2C_front_left.jpg",
    "Honda Fit (imported used)": B + "8/85/Honda_Jazz_Hybrid_Executive_%28IV%29_%E2%80%93_f_18102020.jpg/960px-Honda_Jazz_Hybrid_Executive_%28IV%29_%E2%80%93_f_18102020.jpg",
    "Toyota Aqua (imported used)": B + "d/d8/2017-2021_Toyota_Aqua.jpg/960px-2017-2021_Toyota_Aqua.jpg",
    "Suzuki Cultus VXL": B + "f/f8/2nd_generation_Suzuki_Cultus.jpg/960px-2nd_generation_Suzuki_Cultus.jpg",
    "Suzuki Swift DLX": B + "3/3d/Suzuki_Swift_%282024%29_hybrid_DSC_6076.jpg/960px-Suzuki_Swift_%282024%29_hybrid_DSC_6076.jpg",
    "Toyota Yaris 1.3 GLI": B + "f/f5/2015_Toyota_Yaris_1.5_G_hatchback_%28NCP150R%3B_12-22-2018%29%2C_South_Tangerang.jpg/960px-2015_Toyota_Yaris_1.5_G_hatchback_%28NCP150R%3B_12-22-2018%29%2C_South_Tangerang.jpg",
    "Honda City 1.2L": B + "e/e7/Honda_City_1.5_i-VTEC_V_%28VIII%2C_Facelift%29_%E2%80%93_f_22032025.jpg/960px-Honda_City_1.5_i-VTEC_V_%28VIII%2C_Facelift%29_%E2%80%93_f_22032025.jpg",
    "Toyota Prius S (imported used)": B + "7/71/2018_Toyota_Prius_Excel_VVT-i_CVT_1.8.jpg/960px-2018_Toyota_Prius_Excel_VVT-i_CVT_1.8.jpg",
    "Toyota Corolla Altis 1.6": B + "a/a4/2016_Toyota_Corolla_%28ZRE172R%29_Ascent_sedan_%282017-01-15%29_01.jpg/960px-2016_Toyota_Corolla_%28ZRE172R%29_Ascent_sedan_%282017-01-15%29_01.jpg",
    "Honda Vezel Hybrid (imported used)": B + "7/71/2023_Honda_HR-V_Advance_i-MMD_CVT_1.5.jpg/960px-2023_Honda_HR-V_Advance_i-MMD_CVT_1.5.jpg",
    "MG ZS EV": B + "c/cf/MG_ZS_%28crossover%2C_second_generation%29_DSC_8542.jpg/960px-MG_ZS_%28crossover%2C_second_generation%29_DSC_8542.jpg",
    "Honda Civic Oriel Turbo": B + "6/6d/2017_Honda_Civic_SR_VTEC_1.0_Front.jpg/960px-2017_Honda_Civic_SR_VTEC_1.0_Front.jpg",
    "Kia Sportage Alpha": B + "5/5d/2025_Kia_Sportage_S_front_only.jpg/960px-2025_Kia_Sportage_S_front_only.jpg",
    "Toyota Corolla Cross HEV": B + "4/43/2023_Toyota_Corolla_Cross_XLE_4WD_in_Wind_Chill_Pearl%2C_front_left.jpg/960px-2023_Toyota_Corolla_Cross_XLE_4WD_in_Wind_Chill_Pearl%2C_front_left.jpg",
    "MG HS": B + "3/38/MG_HS_Hybrid%2B_Luxury_%28II%29_%E2%80%93_f_12032026.jpg/960px-MG_HS_Hybrid%2B_Luxury_%28II%29_%E2%80%93_f_12032026.jpg",
    "Hyundai Tucson": B + "6/61/Hyundai_Tucson_1.6_T-GDI_PHEV_Prime_%28IV%29_%E2%80%93_f_05072025.jpg/960px-Hyundai_Tucson_1.6_T-GDI_PHEV_Prime_%28IV%29_%E2%80%93_f_05072025.jpg",
    "BYD Atto 3": B + "3/3e/BYD_Atto_3_1X7A6491.jpg/960px-BYD_Atto_3_1X7A6491.jpg",
    "Honda Civic RS e:HEV": Civic22,
    "Kia Sorento": B + "8/84/2024_Kia_Sorento_X-Line_SX_Prestige_%28facelift%29%2C_front_12.20.24.jpg/960px-2024_Kia_Sorento_X-Line_SX_Prestige_%28facelift%29%2C_front_12.20.24.jpg",
    "Hyundai Santa Fe": B + "e/e6/2024_Hyundai_Santa_Fe_Luxury_AWD_in_Hampton_Grey%2C_front_left%2C_2024-06-30.jpg/960px-2024_Hyundai_Santa_Fe_Luxury_AWD_in_Hampton_Grey%2C_front_left%2C_2024-06-30.jpg",
    "Toyota Fortuner": B + "6/66/2015_Toyota_Fortuner_%28New_Zealand%29.jpg/960px-2015_Toyota_Fortuner_%28New_Zealand%29.jpg",
    "Tesla Model 3 (imported used)": B + "a/ab/Tesla_Model_3_%282023%29_Autofr%C3%BChling_Ulm_IMG_9282.jpg/960px-Tesla_Model_3_%282023%29_Autofr%C3%BChling_Ulm_IMG_9282.jpg",
    "BMW 5 Series (imported used)": B + "8/86/BMW_G60_520i_1X7A2443.jpg/960px-BMW_G60_520i_1X7A2443.jpg",
    "Mercedes-Benz E-Class (imported used)": B + "f/fd/Mercedes-Benz_W214_1X7A1841.jpg/960px-Mercedes-Benz_W214_1X7A1841.jpg",
    "Audi e-tron 50 (imported used)": B + "d/d5/2020_Audi_e-Tron_Sport_50_Quattro.jpg/960px-2020_Audi_e-Tron_Sport_50_Quattro.jpg",
    "Audi A6 45 TFSI (imported used)": B + "e/eb/Audi_A6_C9_IAA_2025_DSC_1920.jpg/960px-Audi_A6_C9_IAA_2025_DSC_1920.jpg",
    "Toyota Land Cruiser Prado (imported used)": B + "e/e8/2024_Toyota_Land_Cruiser_250_VX_in_Platinum_White_Pearl_Mica%2C_front_left.jpg/960px-2024_Toyota_Land_Cruiser_250_VX_in_Platinum_White_Pearl_Mica%2C_front_left.jpg",
    "Range Rover Sport (imported used)": B + "a/aa/2015_Land_Rover_Range_Rover_Sport_HSE_3.0_Front.jpg/960px-2015_Land_Rover_Range_Rover_Sport_HSE_3.0_Front.jpg",
    "Lexus LX 570 (imported used)": B + "3/34/2018_Lexus_LX_570_%28facelift%29%2C_front_3.24.23.jpg/960px-2018_Lexus_LX_570_%28facelift%29%2C_front_3.24.23.jpg",
    "Mercedes-Benz S-Class (imported)": B + "0/09/2026_Mercedes-Benz_V223_IMG_7632.jpg/960px-2026_Mercedes-Benz_V223_IMG_7632.jpg",
    "Toyota Land Cruiser (imported)": B + "6/6d/2021_Toyota_Land_Cruiser_300_3.4_ZX_%28Colombia%29_front_view_04.png/960px-2021_Toyota_Land_Cruiser_300_3.4_ZX_%28Colombia%29_front_view_04.png",
    "Rolls-Royce Cullinan (imported)": B + "0/0d/2019_Rolls-Royce_Cullinan_V12_Automatic_6.75_Front.jpg/960px-2019_Rolls-Royce_Cullinan_V12_Automatic_6.75_Front.jpg",
    # ---------------- bus / truck ----------------
    "Isuzu NPR Truck": B + "6/6e/Nippon_Rent-A-Car_Isuzu_Elf_NJR85A.jpg/960px-Nippon_Rent-A-Car_Isuzu_Elf_NJR85A.jpg",
    "Passenger Bus (Hino class)": B + "8/84/LTZ1328-19-20241030-160332.jpg/960px-LTZ1328-19-20241030-160332.jpg",
    # ---------------- boats ----------------
    "Motor Boat (small)": Motorboat,
    "Speed Boat 200HP": Motorboat,
    "Jet Ski (Yamaha class)": B + "1/17/Couple_of_teenagers_riding_a_jetski_splashing_on_the_Mekong_in_Laos.jpg/960px-Couple_of_teenagers_riding_a_jetski_splashing_on_the_Mekong_in_Laos.jpg",
    "Fishing Trawler (small)": B + "3/30/Trawler_Skagen_harbour.jpg/960px-Trawler_Skagen_harbour.jpg",
    "Catamaran Sailing Boat (imported)": B + "d/d1/Bladef16-1up.jpg/640px-Bladef16-1up.jpg",
    "Luxury Yacht (small)": B + "e/ef/White_Pearl_A_Seite.JPG/960px-White_Pearl_A_Seite.JPG",
    # ---------------- helicopters ----------------
    "Robinson R22 Helicopter": B + "5/54/R22_N4044D_%28cropped%29.jpg/640px-R22_N4044D_%28cropped%29.jpg",
    "Robinson R44 Helicopter": B + "d/d5/Robinson_R44_II_%28cropped%29.jpg/960px-Robinson_R44_II_%28cropped%29.jpg",
    "Robinson R66 Turbine Helicopter": B + "b/be/Robinson_R66_G-CIZG.jpg/960px-Robinson_R66_G-CIZG.jpg",
    "Bell 407 Helicopter": B + "4/4e/Nassau_County_Police_Bell_407.jpg/960px-Nassau_County_Police_Bell_407.jpg",
    "Airbus H125 Helicopter": B + "7/70/RAN_squirrel_helicopter_at_melb_GP_08.jpg/960px-RAN_squirrel_helicopter_at_melb_GP_08.jpg",
    "Airbus H145 Helicopter": B + "a/ab/Stanford_EC145.jpg/960px-Stanford_EC145.jpg",
    "Leonardo AW109 Trekker": B + "4/4e/RAF_A109.jpg/960px-RAF_A109.jpg",
    "Sikorsky S-76 (used)": B + "7/74/Pesca_1_%283737941060%29.jpg/960px-Pesca_1_%283737941060%29.jpg",
    # ---------------- aircraft ----------------
    "Piper PA-28 Cherokee (used)": B + "1/17/G-AVRZ_Piper_PA-28-180_Cherokee_C_at_Northrepps.jpg/960px-G-AVRZ_Piper_PA-28-180_Cherokee_C_at_Northrepps.jpg",
    "Cessna 172 Skyhawk": C172,
    "Diamond DA40 (used)": B + "c/c1/Diamond_DA40_%288736184864%29.jpg/960px-Diamond_DA40_%288736184864%29.jpg",
    "Cessna 182 Skylane": B + "9/9e/Cessna182t_skylane_n2231f_cotswoldairshow_2010_arp.jpg/960px-Cessna182t_skylane_n2231f_cotswoldairshow_2010_arp.jpg",
    # ---------------- jets ----------------
    "Cessna Citation M2 Light Jet": M2,
    "Embraer Phenom 300E": B + "8/8f/Embraer_505_Phenom_300%2C_Aerojet_JP7625910.jpg/960px-Embraer_505_Phenom_300%2C_Aerojet_JP7625910.jpg",
    "Gulfstream G650 Private Jet": B + "d/d6/G-ULFS_Gulfstream_G650_CVT_05-05-16_%2827046023031%29_%28cropped%29.jpg/960px-G-ULFS_Gulfstream_G650_CVT_05-05-16_%2827046023031%29_%28cropped%29.jpg",
    "Bombardier Global 7500": B + "c/cc/N182QS-Global7500-120823.png/960px-N182QS-Global7500-120823.png",
    "Boeing Business Jet (BBJ 737)": B + "3/37/N349BA%40FRA%3B09.07.2010_581ib_%284783401866%29.jpg/960px-N349BA%40FRA%3B09.07.2010_581ib_%284783401866%29.jpg",
}


def image_for(name, category):
    """Photo URL for a vehicle; falls back to its category photo, then ''."""
    return VEHICLE_IMAGES.get(name) or CATEGORY_IMAGES.get(category, "")
