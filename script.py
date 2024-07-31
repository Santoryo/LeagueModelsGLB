import os
import json
from pygltflib import GLTF2

# SETTINGS
ROOT = "C:/Users/lucy/Desktop/LolBinary"
LOL2GLTF = "C:/Users/lucy/Desktop/conv/lol2gltf.exe"



CHAMPIONS = os.listdir(f"{ROOT}/assets/characters")
champ = "zyra"

def getLastPart(path):
    return path.split("/").pop().lower()

# for champ in CHAMPIONS:
dir = os.listdir(f"{ROOT}/assets/characters/{champ}")
os.makedirs(f"./champions/{champ}", exist_ok=True)
if 'skins' in dir:
    skins = os.listdir(f"{ROOT}/assets/characters/{champ}/skins")
    for skin in skins:
        if os.path.exists(f"./champions/{champ}/{skin}.glb"):
            print(f"Skipping {champ} {skin}...")
            continue
        
        print(f"Processing {champ} {skin}...")
        
        data = json.load(open(f"./Out/{champ}/skins/{skin.replace("skin0", "skin").replace('base', 'skin0')}.bin.json"))
        skinMeshProperties = data[f"Characters/{champ.capitalize()}/Skins/{skin.replace("skin0", "skin").replace('base', 'skin0').capitalize()}"]['skinMeshProperties']
        
        path = f"{ROOT}/assets/characters/{champ}/skins/{skin}/"
        
        animPath = data[f"Characters/{champ.capitalize()}/Skins/{skin.replace("skin0", "skin").replace('base', 'skin0').capitalize()}"]
        if not os.path.exists(f"{path}animations"):
            animPath = f"{ROOT}/assets/characters/{champ}/skins/base/animations"
        else:
            animPath = f"{path}animations"
        
        output = f"./champions/{champ}/{skin}.glb"
        commandWithoutAnims = f'{LOL2GLTF} skn2gltf --skn "{ROOT}/{skinMeshProperties["simpleSkin"].lower()}" --skl "{ROOT}/{skinMeshProperties["skeleton"].lower()}" -g "{output}"'
        os.system(commandWithoutAnims)
        
        gltf = GLTF2().load(output)
        mats = gltf.materials
        
        textures = []
        materials = []
        
        for i, material in enumerate(mats):
            materials.append(f'"{material.name}"')
            txt = f"{ROOT}/{skinMeshProperties["texture"].lower()}"
            if "materialOverride" in skinMeshProperties:
                for materialOvveride in skinMeshProperties["materialOverride"]:
                    if materialOvveride["submesh"] == material.name:
                        txt = f"{ROOT}/{materialOvveride['texture'].lower()}"
            textures.append(f'"{txt}"')
            
        command = f'{LOL2GLTF} skn2gltf --skn "{ROOT}/{skinMeshProperties["simpleSkin"].lower()}" --skl "{ROOT}/{skinMeshProperties["skeleton"].lower()}" -g "{output}" -a "{animPath}" --materials {" ".join(materials)} --textures {" ".join(textures)}'
        
        print(command)
        os.system(command)
        os.system(f"gltf-transform optimize {output} {output} --compress draco --texture-compress webp")
    
    
