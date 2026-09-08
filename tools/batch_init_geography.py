import os

topics = [
    # Part A — Foundations (Cl.6)
    ("part_a_foundations", "01_earth_in_solar_system", "Earth in the Solar System"),
    ("part_a_foundations", "02_globe_lat_long_motions", "Globe, Latitudes & Longitudes, Motions of Earth"),
    ("part_a_foundations", "03_maps_and_map_skills", "Maps & Map Skills"),
    ("part_a_foundations", "04_major_domains_landforms", "Major Domains & Landforms of the Earth"),
    
    # Part B — Physical Geography Systems (Cl.7 + Cl.11 Fundamentals)
    ("part_b_physical_systems", "05_earth_interior_rocks_quakes_volcanoes", "Earth's Interior, Rocks, Earthquakes & Volcanoes"),
    ("part_b_physical_systems", "06_landforms_geomorphic_processes", "Landforms & Geomorphic Processes"),
    ("part_b_physical_systems", "07_atmosphere_insolation_temperature", "Atmosphere, Insolation & Temperature"),
    ("part_b_physical_systems", "08_atmospheric_circulation_weather_systems", "Atmospheric Circulation & Weather Systems"),
    ("part_b_physical_systems", "09_humidity_precip_climates_climate_change", "Humidity, Precipitation, World Climates & Climate Change"),
    ("part_b_physical_systems", "10_oceans_ocean_water_movements", "Oceans & Ocean Water Movements"),
    ("part_b_physical_systems", "11_natural_vegetation_wildlife_biomes", "Natural Vegetation, Wildlife & Biomes"),
    ("part_b_physical_systems", "12_natural_hazards_disasters", "Natural Hazards & Disasters"),
    
    # Part C — World Human-Environment Regions (Cl.7)
    ("part_c_world_human_env", "13_human_settlements_transport_comm_world", "Human Settlements, Transport & Communication (World)"),
    ("part_c_world_human_env", "14_life_tropical_temperate_desert", "Life in Tropical, Temperate Grassland & Desert Regions"),
    
    # Part D — India's Physical Geography (Cl.9 + Cl.11 India)
    ("part_d_india_physical", "15_india_location_size_physiography", "India: Location, Size & Physiography"),
    ("part_d_india_physical", "16_drainage_systems_india", "Drainage Systems of India"),
    ("part_d_india_physical", "17_climate_of_india", "Climate of India"),
    ("part_d_india_physical", "18_natural_veg_wildlife_india", "Natural Vegetation & Wildlife of India"),
    
    # Part E — India's Resources & Economy (Cl.8 + Cl.10)
    ("part_e_india_resources_economy", "19_resources_concept_types_planning", "Resources: Concept, Types & Planning"),
    ("part_e_india_resources_economy", "20_land_soil_water_resources_india", "Land, Soil & Water Resources of India"),
    ("part_e_india_resources_economy", "21_mineral_power_resources_india", "Mineral & Power Resources of India"),
    ("part_e_india_resources_economy", "22_agriculture_in_india", "Agriculture in India"),
    ("part_e_india_resources_economy", "23_manufacturing_industries_india", "Manufacturing Industries in India"),
    ("part_e_india_resources_economy", "24_population_human_resources_india", "Population & Human Resources of India"),
    ("part_e_india_resources_economy", "25_lifelines_national_economy", "Lifelines of the National Economy"),
    
    # Part F — World Human Geography (Cl.12 Fundamentals)
    ("part_f_world_human_geography", "26_human_geography_nature_scope", "Human Geography: Nature & Scope"),
    ("part_f_world_human_geography", "27_world_population", "World Population"),
    ("part_f_world_human_geography", "28_human_development", "Human Development"),
    ("part_f_world_human_geography", "29_primary_activities", "Primary Activities"),
    ("part_f_world_human_geography", "30_secondary_activities", "Secondary Activities"),
    ("part_f_world_human_geography", "31_tertiary_quaternary_activities", "Tertiary & Quaternary Activities"),
    ("part_f_world_human_geography", "32_transport_comm_world", "Transport & Communication (World)"),
    ("part_f_world_human_geography", "33_international_trade", "International Trade"),
    
    # Part G — India: People and Economy (Cl.12)
    ("part_g_india_people_economy", "34_population_of_india", "Population of India"),
    ("part_g_india_people_economy", "35_human_settlements_india", "Human Settlements in India"),
    ("part_g_india_people_economy", "36_land_resources_agri_adv", "Land Resources & Agriculture (Advanced)"),
    ("part_g_india_people_economy", "37_water_resources_adv", "Water Resources (Advanced)"),
    ("part_g_india_people_economy", "38_mineral_energy_resources_adv", "Mineral & Energy Resources (Advanced)"),
    ("part_g_india_people_economy", "39_manufacturing_industries_adv", "Manufacturing Industries (Advanced)"),
    ("part_g_india_people_economy", "40_transport_comm_india", "Transport & Communication in India"),
    ("part_g_india_people_economy", "41_international_trade_india", "International Trade of India"),
    ("part_g_india_people_economy", "42_geographical_perspective_issues", "Geographical Perspective on Selected Issues"),
]

def init_all():
    base_root = os.path.join("content", "02_geography")
    for part, slug, title in topics:
        folder = os.path.join(base_root, part, slug)
        assets = os.path.join(folder, "assets")
        os.makedirs(assets, exist_ok=True)
        
        files = {
            "raw_notes.md": f"# Raw Notes: {title}\n\n<!-- Paste your MD summary content here -->\n",
            "blueprint.md": f"# Blueprint: {title}\n\n",
            "study_page.md": f"# High-Yield Revision Sheet: {title}\n\n",
            "video_script.md": f"# 60-75s Video Scripts: {title}\n\n",
            "storyboard.md": f"# Storyboard & Prompts: {title}\n\n",
        }
        for name, text in files.items():
            fpath = os.path.join(folder, name)
            if not os.path.exists(fpath):
                with open(fpath, "w", encoding="utf-8") as f:
                    f.write(text)
                    
    print(f"✅ Successfully initialized all 42 topic folders under {base_root}!")

if __name__ == "__main__":
    init_all()