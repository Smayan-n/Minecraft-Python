from ursina import *
from ursina.prefabs.first_person_controller import FirstPersonController
import random

app = Ursina()

window.title = 'Minecraft!'
window.borderless = False
window.fullscreen = False
window.exit_button.visible = False


wood_texture = load_texture('assets/wood.jpg')
grass_texture = load_texture('assets/grass_block.png')
stone_texture = load_texture('assets/stone_block.png')
brick_texture = load_texture('assets/brick_block.png')
dirt_texture = load_texture('assets/dirt_block.png')
sky_texture = load_texture('assets/skybox.png')
arm_texture = load_texture('assets/arm_texture.png')
glass_texture = load_texture('assets/glass.png')
leaf_texture = load_texture('assets/leaf.jpg')

block_pick = 1
escape = False

def update():
	global block_pick, escape


	if held_keys['left mouse'] or held_keys['right mouse']:
		arm.active()
	else:
		arm.normal()

	if held_keys['1']: 
		block_pick = 1
	if held_keys['2']:  
		block_pick = 2
	if held_keys['3']:
		block_pick = 3
	if held_keys['4']: 
		block_pick = 4
	if held_keys['5']: 
		block_pick = 5
	if held_keys['6']: 
		block_pick = 6

	if held_keys['escape']:
		player.on_disable()
	if held_keys['tab']:
		player.on_enable()

	#prevents player from endless falling
	if player.y < -60:
		player.y = 25
		player.x = platform_size / 2
		player.z = platform_size / 2

	#looking for sprint
	if held_keys['left control']:
		player.speed = 10
	else:
		player.speed = 6.5



class Voxel(Button):
	def __init__(self, position = (0, 0 ,0), texture = grass_texture):
		super().__init__(
			parent = scene,
			model = 'assets/block',
			position = position,
			origin_y = 1,
			texture = texture,
			color = color.color(0, 0, random.uniform(0.85, 1)),
			scale = 0.5,
			highlight_color = color.rgb(191, 191, 191),
			double_sided = True,
			)

	def input(self, key):
		global block_pick

		#pick block
		if self.hovered:
			if key == "middle mouse down":
				if self.texture == grass_texture:
					block_pick = 1
				if self.texture == dirt_texture:
					block_pick = 2
				if self.texture == stone_texture:
					block_pick = 3
				if self.texture == brick_texture:
					block_pick = 4
				if self.texture == wood_texture:
					block_pick = 5
				if self.texture == leaf_texture:
					block_pick = 6

		if self.hovered:
			if key == "right mouse down":
				if block_pick == 1:voxel = Voxel(position = self.position + mouse.normal, texture = grass_texture)
				if block_pick == 2:voxel = Voxel(position = self.position + mouse.normal, texture = dirt_texture)
				if block_pick == 3:voxel = Voxel(position = self.position + mouse.normal, texture = stone_texture)
				if block_pick == 4:voxel = Voxel(position = self.position + mouse.normal, texture = brick_texture)
				if block_pick == 5:voxel = Voxel(position = self.position + mouse.normal, texture = wood_texture)
				if block_pick == 6:voxel = Voxel(position = self.position + mouse.normal, texture = leaf_texture)

		if self.hovered:
			if key == "left mouse down":
				destroy(self)



class sky(Entity):
	def __init__(self):
		super().__init__(
			parent = scene,
			model = 'sphere',
			texture = sky_texture,
			position = Vec3(platform_size/2, 0, platform_size/2),
			scale = 120,
			double_sided = True
			)

class Sun(Entity):
	def __init__(self):
		super().__init__(
			parent = scene,
			model = 'quad',
			color = color.yellow,
			scale = 10,
			double_sided = True,
			position = (8, 50, 8),
			rotation = (90, 90, 0),

			)




class hand(Entity):
	def __init__(self):
		super().__init__(
			parent = camera.ui,
			model = 'assets/arm',
			texture = arm_texture,
			scale = 0.2,
			rotation = (150, -10, 0),
			position = (0.5, -0.6)
			)

	def active(self):
		self.rotation = (150, -20, 0)
		self.position = (0.4, -0.5)

	def normal(self):
		self.rotation = (150, -10, 0)
		self.position = (0.5, -0.6)


class Held_block(Entity):
	def __init__(self, texture = grass_texture):
		super().__init__(
			parent = camera.ui,
			model = 'assets/block',
			texture = texture,
			scale = 0.1,
			rotation = (-25, 30, 0),
			position = (0.28, -0.16)
			)

	def input(self, key):
			if block_pick == 1:
				destroy(self)
				held_block = Held_block(texture = grass_texture)
			if block_pick == 2:
				destroy(self)
				held_block = Held_block(texture = dirt_texture)
			if block_pick == 3: 
				destroy(self)
				held_block = Held_block(texture = stone_texture)
			if block_pick == 4: 
				destroy(self)
				held_block = Held_block(texture = brick_texture)
			if block_pick == 5: 
				destroy(self)
				held_block = Held_block(texture = wood_texture)
			if block_pick == 6: 
				destroy(self)
				held_block = Held_block(texture = leaf_texture)


#creating the main platform
platform_size = 16
for z in range(platform_size):
	for x in range(platform_size):
		voxel = Voxel(position = (x, 0 ,z))
		


#creating trees
for count in range(3):

	startPos_x = random.randrange(platform_size)
	startPos_z = random.randrange(platform_size)

	for y in range(1,6):
		voxel = Voxel(position = (startPos_x, y ,startPos_z), texture = wood_texture)

	for z in range(startPos_z, startPos_z + 5):
		for x in range(startPos_x, startPos_x + 5):
			voxel = Voxel(position = (x - 2 , y , z - 2), texture = leaf_texture)
		
	for z in range(startPos_z, startPos_z + 3):
		for x in range(startPos_x, startPos_x + 3):
			voxel = Voxel(position = (x - 1 , y + 1, z - 1), texture = leaf_texture)
		
	voxel = Voxel(position = (startPos_x , y + 2, startPos_z), texture = leaf_texture)

#making crosshair
crossHair1 = Entity(parent = camera.ui, model = 'cube', scale = (0.005, 0.03), color = color.red)
crossHair2 = duplicate(crossHair1, rotation = (0, 0, 90))

skybox = sky()
sun = Sun()
arm = hand()
held_block = Held_block()

player = FirstPersonController(mouse_sensitivity = (85, 85), speed = 6.5)

app.run()