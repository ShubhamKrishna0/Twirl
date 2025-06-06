from typing import List, Tuple
from langchain_anthropic import ChatAnthropic
from langchain_core.messages import HumanMessage, AIMessage, BaseMessage
from langgraph.prebuilt import create_react_agent
from parser import extract_relevant_part
import base64
import httpx
import os
from dotenv import load_dotenv

load_dotenv()

def encode_image(image_url: str) -> Tuple[str, str]:
    response = httpx.get(image_url)
    image_data = base64.b64encode(response.content).decode('utf-8')
    media_type = response.headers.get('content-type', 'image/jpeg')
    return image_data, media_type

model = ChatAnthropic(
    model="claude-3-5-sonnet-20241022",
    max_tokens=8192,
    temperature=1,
    anthropic_api_key=os.environ.get("ANTHROPIC_API_KEY")
)

tools = []

agent_graph = create_react_agent(
    model,
    tools,
)

def create_message_with_image(prompt1: str, prompt2: str, image_url: str) -> List[BaseMessage]:
    image_data, media_type = encode_image(image_url)
    
    return [
        HumanMessage(content=[
            {
                "type": "text",
                "text": prompt1
            },
            {
                "type": "text",
                "text": prompt2
            },
            {
                "type": "image",
                "source": {
                    "type": "base64",
                    "media_type": media_type,
                    "data": image_data
                }
            }
        ]),
        AIMessage(content=[
            {
                "type": "text",
                "text": "<model_planning>"
            }
        ])
    ]


async def main():
    description = "Generate a model of pine tree."
    image_url = "https://media.sketchfab.com/models/c1d140fc15bd40928989d0ca79365e13/thumbnails/465f602c45454d8f813cc54198930c24/76d9c131a5314d98bf271617a3a43378.jpeg"
    
    messages = create_message_with_image(
        "<examples>\n<example>\n<description>\nGenerate a model of a hollow cylinder with a 5mm wall thickness\n</description>\n<ideal_output>\n<model_planning>\n1. Extract features and relationships:\n   - Shape: cylinder (hollow)\n   - Outer radius: 20 units\n   - Wall thickness: 5 units\n   - Height: 40 units\n   - Relationship: cylinder is centered\n\n2. Organize features into a structured plan:\n   a. Create a scene, camera, and renderer\n   b. Create a hollow cylinder using THREE.CylinderGeometry\n   c. Position the cylinder at the center of the scene\n   d. Set up lighting\n   e. Set up animation loop\n\n3. Basic structure of the Three.js script:\n   - Import Three.js library\n   - Set up scene, camera, and renderer\n   - Create cylinder geometry and material\n   - Add cylinder to the scene\n   - Set up lighting\n   - Define animation loop\n   - Handle window resizing\n\n4. Materials and textures:\n   - Use MeshStandardMaterial for realistic lighting and shadows\n   - Apply a metallic texture to give the cylinder a realistic appearance\n\n5. Lighting setup:\n   - Add ambient light for overall illumination\n   - Add directional light for shadows and depth\n   - Add point light inside the cylinder to highlight the hollow nature\n\n6. Potential animations:\n   - Rotate the cylinder to showcase its hollow structure\n\n7. Potential challenges and solutions:\n   - Creating a hollow cylinder: Use THREE.CylinderGeometry with inner radius\n   - Ensuring the hollow part is visible: Use camera controls to allow user interaction\n\n8. Summary of structured plan:\n   The plan involves creating a scene with a hollow cylinder using Three.js. The cylinder will have an outer radius of 20 units, a wall thickness of 5 units, and a height of 40 units. It will be centered in the scene and use a metallic material. Lighting will be set up to properly illuminate the model, including the hollow interior. An animation will be added to rotate the model, and camera controls will allow for user interaction to better visualize the hollow structure.\n</model_planning>\n\n<threejs_output>\n// Hollow Cylinder Model\n// Dimensions: Outer radius 20 units, Wall thickness 5 units, Height 40 units\n\n// Scene setup\nconst scene = new THREE.Scene();\nconst camera = new THREE.PerspectiveCamera(75, window.innerWidth / window.innerHeight, 0.1, 1000);\nconst renderer = new THREE.WebGLRenderer();\nrenderer.setSize(window.innerWidth, window.innerHeight);\ndocument.body.appendChild(renderer.domElement);\n\n// Cylinder\nconst outerRadius = 20;\nconst innerRadius = 15; // outer radius - wall thickness\nconst height = 40;\nconst radialSegments = 32;\nconst cylinderGeometry = new THREE.CylinderGeometry(outerRadius, outerRadius, height, radialSegments, 1, true, 0, Math.PI * 2);\nconst cylinderMaterial = new THREE.MeshStandardMaterial({ \n  color: 0x888888, \n  metalness: 0.8,\n  roughness: 0.2,\n  side: THREE.DoubleSide\n});\nconst cylinder = new THREE.Mesh(cylinderGeometry, cylinderMaterial);\nscene.add(cylinder);\n\n// Lighting\nconst ambientLight = new THREE.AmbientLight(0x404040);\nscene.add(ambientLight);\nconst directionalLight = new THREE.DirectionalLight(0xffffff, 0.5);\ndirectionalLight.position.set(1, 1, 1);\nscene.add(directionalLight);\nconst pointLight = new THREE.PointLight(0xffffff, 0.5);\npointLight.position.set(0, 0, 0);\nscene.add(pointLight);\n\n// Camera position\ncamera.position.z = 100;\n\n// Orbit controls\nconst controls = new THREE.OrbitControls(camera, renderer.domElement);\n\n// Animation\nfunction animate() {\n  requestAnimationFrame(animate);\n  cylinder.rotation.y += 0.01;\n  controls.update();\n  renderer.render(scene, camera);\n}\nanimate();\n\n// Handle window resizing\nwindow.addEventListener('resize', function() {\n  camera.aspect = window.innerWidth / window.innerHeight;\n  camera.updateProjectionMatrix();\n  renderer.setSize(window.innerWidth, window.innerHeight);\n});\n</threejs_output>\n</ideal_output>\n</example>\n<example>\n<description>\nCreate a dining table\n</description>\n<ideal_output>\n<model_planning>\n1. Extract features and relationships:\n   - Main components: tabletop, legs, support structure\n   - Standard dining table dimensions:\n     * Tabletop: ~150cm length, ~90cm width, ~4cm thickness\n     * Height: ~75cm (standard dining height)\n     * Legs: ~8cm square thickness\n     * Support rails: ~5cm height, ~3cm thickness\n     * Support positioning: ~20cm below tabletop\n\n2. Organize features into a structured plan:\n   a. Create a scene, camera, and renderer\n   b. Create tabletop as a BoxGeometry\n   c. Create four legs as BoxGeometry\n   d. Create support rails as BoxGeometry\n   e. Group all components into a single Object3D\n   f. Position components correctly\n   g. Set up lighting\n   h. Set up animation loop and controls\n\n3. Basic structure of Three.js script:\n   - Import Three.js library\n   - Set up scene, camera, and renderer\n   - Define all dimensional variables\n   - Create functions for table components (tabletop, leg, support rail)\n   - Create and position all components\n   - Group components into a table object\n   - Set up lighting\n   - Set up orbit controls for interaction\n   - Define animation loop\n   - Handle window resizing\n\n4. Materials and textures:\n   - Use MeshStandardMaterial for realistic lighting and shadows\n   - Apply wood texture to all components\n\n5. Lighting setup:\n   - Add ambient light for overall illumination\n   - Add directional light for shadows and depth\n   - Add point lights to highlight details\n\n6. Potential animations:\n   - Rotate the table to showcase its structure\n   - Allow user interaction with orbit controls\n\n7. Potential challenges and solutions:\n   - Correct positioning of components: Use careful calculations and Three.js positioning\n   - Realistic wood appearance: Use texture mapping\n   - Performance with complex geometry: Use appropriate level of detail\n\n8. Summary of structured plan:\n   Create a Three.js scene with a dining table, including tabletop, legs, and support structure. Use realistic dimensions and wood textures. Set up proper lighting to showcase the table's features. Implement orbit controls for user interaction and add subtle animation to rotate the table.\n</model_planning>\n\n<threejs_output>\n// Dining Table Model\n// All dimensions in centimeters\n\n// Scene setup\nconst scene = new THREE.Scene();\nconst camera = new THREE.PerspectiveCamera(75, window.innerWidth / window.innerHeight, 0.1, 1000);\nconst renderer = new THREE.WebGLRenderer();\nrenderer.setSize(window.innerWidth, window.innerHeight);\ndocument.body.appendChild(renderer.domElement);\n\n// Dimensions\nconst tableLength = 150;\nconst tableWidth = 90;\nconst tableHeight = 75;\nconst topThickness = 4;\nconst legWidth = 8;\nconst legInset = 5;\nconst supportHeight = 5;\nconst supportThickness = 3;\n\n// Materials\nconst woodTexture = new THREE.TextureLoader().load('wood_texture.jpg');\nconst woodMaterial = new THREE.MeshStandardMaterial({ map: woodTexture });\n\n// Table components\nfunction createTabletop() {\n  const geometry = new THREE.BoxGeometry(tableLength, topThickness, tableWidth);\n  return new THREE.Mesh(geometry, woodMaterial);\n}\n\nfunction createLeg() {\n  const geometry = new THREE.BoxGeometry(legWidth, tableHeight - topThickness, legWidth);\n  return new THREE.Mesh(geometry, woodMaterial);\n}\n\nfunction createSupportRail(length) {\n  const geometry = new THREE.BoxGeometry(length, supportHeight, supportThickness);\n  return new THREE.Mesh(geometry, woodMaterial);\n}\n\n// Create table\nconst table = new THREE.Object3D();\n\n// Tabletop\nconst tabletop = createTabletop();\ntabletop.position.y = tableHeight - topThickness / 2;\ntable.add(tabletop);\n\n// Legs\nconst legPositions = [\n  { x: -tableLength/2 + legInset + legWidth/2, z: -tableWidth/2 + legInset + legWidth/2 },\n  { x: tableLength/2 - legInset - legWidth/2, z: -tableWidth/2 + legInset + legWidth/2 },\n  { x: -tableLength/2 + legInset + legWidth/2, z: tableWidth/2 - legInset - legWidth/2 },\n  { x: tableLength/2 - legInset - legWidth/2, z: tableWidth/2 - legInset - legWidth/2 }\n];\n\nlegPositions.forEach(pos => {\n  const leg = createLeg();\n  leg.position.set(pos.x, (tableHeight - topThickness) / 2, pos.z);\n  table.add(leg);\n});\n\n// Support rails\nconst longRailLength = tableLength - 2 * legInset - 2 * legWidth;\nconst shortRailLength = tableWidth - 2 * legInset - 2 * legWidth;\n\nconst longRailPositions = [\n  { x: 0, z: -tableWidth/2 + legInset + legWidth/2 },\n  { x: 0, z: tableWidth/2 - legInset - legWidth/2 }\n];\n\nconst shortRailPositions = [\n  { x: -tableLength/2 + legInset + legWidth/2, z: 0 },\n  { x: tableLength/2 - legInset - legWidth/2, z: 0 }\n];\n\nlongRailPositions.forEach(pos => {\n  const rail = createSupportRail(longRailLength);\n  rail.position.set(pos.x, tableHeight - topThickness - supportHeight - 20, pos.z);\n  table.add(rail);\n});\n\nshortRailPositions.forEach(pos => {\n  const rail = createSupportRail(shortRailLength);\n  rail.rotation.y = Math.PI / 2;\n  rail.position.set(pos.x, tableHeight - topThickness - supportHeight - 20, pos.z);\n  table.add(rail);\n});\n\nscene.add(table);\n\n// Lighting\nconst ambientLight = new THREE.AmbientLight(0x404040);\nscene.add(ambientLight);\n\nconst directionalLight = new THREE.DirectionalLight(0xffffff, 0.5);\ndirectionalLight.position.set(1, 1, 1);\nscene.add(directionalLight);\n\nconst pointLight1 = new THREE.PointLight(0xffffff, 0.5);\npointLight1.position.set(0, 100, 0);\nscene.add(pointLight1);\n\nconst pointLight2 = new THREE.PointLight(0xffffff, 0.3);\npointLight2.position.set(100, 0, 100);\nscene.add(pointLight2);\n\n// Camera position\ncamera.position.set(150, 100, 150);\ncamera.lookAt(scene.position);\n\n// Orbit controls\nconst controls = new THREE.OrbitControls(camera, renderer.domElement);\n\n// Animation\nfunction animate() {\n  requestAnimationFrame(animate);\n  table.rotation.y += 0.002;\n  controls.update();\n  renderer.render(scene, camera);\n}\nanimate();\n\n// Handle window resizing\nwindow.addEventListener('resize', function() {\n  camera.aspect = window.innerWidth / window.innerHeight;\n  camera.updateProjectionMatrix();\n  renderer.setSize(window.innerWidth, window.innerHeight);\n});\n</threejs_output>\n</ideal_output>\n</example>\n</examples>\n\n",
        f"You are Imagine3D, an expert AI assistant specializing in generating accurate, error-free Three.js scripts based on textual descriptions or images of 3D objects. Your task is to create precise, functional 3D models that can be directly used in a Three.js environment.\n\nHere is the description of the 3D object you need to model:\n\n<description>\n{description}\n</description>\n\nPlease follow these guidelines to create the Three.js script:\n\n1. Analyze the Input:\n   - For textual descriptions, carefully extract all dimensions, shapes, features, and spatial relationships.\n   - For images, if mentioned, interpret the 3D structure as accurately as possible.\n\n2. Use Three.js Best Practices:\n   - Use valid Three.js syntax only.\n   - Utilize appropriate geometries, materials, and lighting.\n   - Ensure the scene is properly set up with camera and renderer.\n   - Avoid redundant or unused components in the script.\n   - Ensure readability and maintainability.\n\n3. Dimensions and Units:\n   - Use appropriate units for Three.js (typically scene units).\n   - If units are ambiguous, make reasonable assumptions based on context.\n   - When given ranges, use random but realistic values within the specified range.\n\n4. Script Structure:\n   - Use 2 spaces for indentation.\n   - Organize the script into logical sections:\n     a. Scene, camera, and renderer setup\n     b. Geometry and material creation\n     c. Object positioning and scaling\n     d. Lighting setup\n     e. Animation (if applicable)\n     f. Render loop\n\n5. Verification:\n   - Check for syntax errors.\n   - Ensure all objects and variables are used correctly.\n   - Validate that the generated script will execute without additional user input.\n\nBefore generating the final output, wrap your model planning inside <model_planning> tags:\n1. Extract all features and relationships from the input.\n2. Organize these features into a structured plan for the Three.js model.\n3. Sketch out the basic structure of the Three.js script, including main objects and functions.\n4. Plan out the materials and textures to be used for each part of the model.\n5. Design the lighting setup, including type, position, and intensity of lights.\n6. Consider potential animations or interactive elements that could enhance the model.\n7. Identify potential challenges in implementing the model and how to address them.\n8. Summarize the structured plan to ensure alignment with the user's intent.\n\nProvide your ThreeJS code inside <threejs_output> tags. \n\nRemember to provide a complete, executable Three.js script that can be directly copied and pasted into a web environment without errors.",
        image_url
    )
    
    result = ""
    async for output in agent_graph.astream({
        "messages": messages,
    }, stream_mode="values"):
        if "messages" in output:
            messages = output["messages"]
            if messages and isinstance(messages[-1], AIMessage):
                result += messages[-1].content

    threejs_code = extract_relevant_part(result)


    # second_response = await model.ainvoke(second_messages)
    # print(f"Analysis: {second_response.content}")

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())