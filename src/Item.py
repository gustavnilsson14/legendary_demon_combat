from Unit import *
from Core import *
from Constants import *
import math
import random


class Item( Entity ) :

    def __init__( self, scene, pos, cooldown = 0, local_anchor = ( 0, 0 ) ) :
        Entity.__init__( self, scene )
        self.body_handler = Body( scene )
        self.position = pos
        self.holder = 0
        self.body = 0
        self.max_cooldown = cooldown
        self.cooldown = 0
        self.local_anchor = local_anchor
        self.fire_rate_multiplier = 1
        self.spawn_point = 0
        self.types += [ "item" ]

    def update( self, update ) :
        if self.cooldown > 0 :
            self.cooldown -= (1 * self.fire_rate_multiplier)

    def use( self ) :
        if self.cooldown <= 0 :
            self.cooldown = self.max_cooldown
            return True
        return False

    def create_body( self ) :
        if self.body == 0 :
            return
        self.scene.game.add_garbage_body( self.body )

    def destroy_body( self ) :
        if self.body != 0 :
            self.scene.game.add_garbage_body( self.body )
            return True
        return False

    def dropped( self ) :
        pass

    def picked( self ) :
        if self.spawn_point != 0 :
            self.spawn_point.entity = 0

class Weapon( Item ) :

    def __init__( self, scene, pos, cooldown, local_anchor, attack_range ) :
        Item.__init__( self, scene, pos, cooldown, local_anchor )
        self.attack_range = attack_range
        self.viable_slots = []
        self.types += [ "weapon" ]

    def use( self, target ) :
        if target == 0 :
            return True
        if get_distance_between_points( self.body.transform.position, target.body.transform.position ) < self.attack_range :
            return True
        return False

    def create_body( self ) :
        Item.create_body( self )

class ProjectileWeapon( Weapon ) :

    def __init__( self, scene, pos, cooldown = 2, local_anchor = (0.45,0), attack_range = 5 ) :
        Weapon.__init__( self, scene, pos, cooldown, local_anchor, attack_range )
        self.attack_range = attack_range
        self.spread = 0
        self.types += [ "projectile_weapon" ]

    def use( self, target ) :
        if Weapon.use( self, target ) :
            if Item.use( self ) :
                self.create_projectile()
                return True
            return True
        return False

    def holder_is_player( self ) :
        if self.holder == 0 :
            return False
        if 'player_character' in self.holder.get_owner_types() :
            return True
        return False

    def create_body( self ) :
        Weapon.create_body( self )

    def handle_collision( self, my_fixture, colliding_fixture ) :
        pass

    def apply_spread( self ) :
        angle = math.radians( math.degrees( self.body.transform.angle ) + random.randint( -self.spread, self.spread ) )
        rotation = b2Rot( angle )
        return b2Transform( self.body.transform.position, rotation )

    def create_projectile( self ) :
        pass

class Shotgun( ProjectileWeapon ) :

    def __init__( self, scene, pos = ( 0, 0 )  ) :
        ProjectileWeapon.__init__( self, scene, pos, 14, (0.3,0), 3 )
        self.pellet_amount = 10
        self.spread = 7
        self.types += [ "shotgun" ]

    def create_projectile( self ) :
        if ProjectileWeapon.holder_is_player( self ) :
            self.scene.screen.shake_time = 6
        if self.body != 0 :
            for i in range(0, self.pellet_amount ) :
                transform = self.apply_spread()
                projectile = Pellet( self.holder.get_owner(), self.scene, transform )
                self.scene.add_entity( projectile )

    def create_body( self, pos ) :
        ProjectileWeapon.create_body( self )
        self.body = self.body_handler.create_short_gun( self, self.scene, pos, 1, FILTER_WEAPON )
        self.body_handler.set_image_at( 'main', 'res/img/weapon/machinegun.png' )
        return self.body

class Machinegun( ProjectileWeapon ) :

    def __init__( self, scene, pos = ( 0, 0 ) ) :
        ProjectileWeapon.__init__( self, scene, pos, 3, (0.4,0), 3 )
        self.spread = 1
        self.types += [ "machinegun" ]

    def create_projectile( self ) :
        if ProjectileWeapon.holder_is_player( self ) :
            self.scene.screen.shake_time = 1
        if self.body != 0 :
            transform = self.apply_spread()
            projectile = Projectile( self.holder.get_owner(), self.scene, transform )
            self.scene.add_entity( projectile )

    def create_body( self, pos ) :
        ProjectileWeapon.create_body( self )
        self.body = self.body_handler.create_long_gun( self, self.scene, pos, 1, FILTER_WEAPON )
        self.body_handler.set_image_at( 'main', 'res/img/weapon/machinegun.png' )
        return self.body

class SpellOrb( ProjectileWeapon ) :

    def __init__( self, scene, pos, cooldown = 2, local_anchor = (0.45,0), attack_range = 5 ) :
        ProjectileWeapon.__init__( self, scene, pos, cooldown, local_anchor, attack_range )
        self.viable_slots = [ 'spell_orb' ]
        self.types += [ "SpellOrb" ]

    def create_projectile( self ) :
        pass

    def create_body( self, pos ) :
        ProjectileWeapon.create_body( self )
        self.body = self.body_handler.create_long_gun( self, self.scene, pos, 1, FILTER_WEAPON )
        self.body_handler.set_image_at( 'main', 'res/img/weapon/machinegun.png' )
        return self.body

    def get_holder_orbs( self ) :
        if ProjectileWeapon.holder_is_player( self ) :
            owner = self.holder.get_owner()
            return owner.orbs
        return 0

    def dropped( self ) :
        self.holder = 1
        self.scene.remove_entity( self )
        self.destroy_body()

    def picked( self, owner, slot ) :
        Item.picked( self )
        if slot == 0 :
            return False
        if slot.item != 0 :
            if self.types[-1] == slot.item.types[-1] :
                if owner.orbs == 3 :
                    return True
                owner.orbs += 1
                self.scene.remove_entity( self )
                self.destroy_body()
                return True
        owner.orbs = 1
        return False

class FireOrb( SpellOrb ) :

    def __init__( self, scene, pos = ( 0, 0 ) ) :
        SpellOrb.__init__( self, scene, pos, 24, (0.15,0), 3 )
        self.types += [ self.__class__.__name__ ]

    def create_body( self, pos ) :
        ProjectileWeapon.create_body( self )
        self.body = self.body_handler.create_orb( self, self.scene, pos, 1, FILTER_WEAPON )
        self.body_handler.set_image_at( 'main', 'res/img/weapon/red_ball.png' )
        return self.body

    def create_projectile( self ) :
        transform = self.apply_spread()
        if ProjectileWeapon.holder_is_player( self ) :
            self.scene.screen.shake_time = 1
        if self.body != 0 :
            if self.get_holder_orbs() == 2 :
                for spread in [-16,16] :
                    angle = math.radians( math.degrees( transform.angle ) + spread )
                    transform = b2Transform( transform.position, b2Rot( angle ) )
                    projectile = FireBall( self.holder.get_owner(), self.scene, transform )
                    self.scene.add_entity( projectile )
                return
            if self.get_holder_orbs() == 3 :
                projectile = FireBallBig( self.holder.get_owner(), self.scene, transform )
                self.scene.add_entity( projectile )
                return
            projectile = FireBall( self.holder.get_owner(), self.scene, transform )
            self.scene.add_entity( projectile )

    def picked( self, owner, slot ) :
        owner.immunities = [ DAMAGE_TYPE_FIRE ]
        owner.body_handler.set_image_at( 'head', 'res/img/body/fire_head.png' )
        owner.body_handler.set_image_at( 'right_arm', 'res/img/body/fire_arm.png' )
        owner.body_handler.set_image_at( 'left_arm', 'res/img/body/fire_arm.png' )
        owner.body_handler.set_image_at( 'right_shoulder', 'res/img/body/fire_shoulder.png' )
        owner.body_handler.set_image_at( 'left_shoulder', 'res/img/body/fire_shoulder.png' )
        return SpellOrb.picked( self, owner, slot )

class IceOrb( SpellOrb ) :

    def __init__( self, scene, pos = ( 0, 0 ) ) :
        SpellOrb.__init__( self, scene, pos, 12, (0.15,0), 3 )
        self.types += [ self.__class__.__name__ ]

    def create_body( self, pos ) :
        ProjectileWeapon.create_body( self )
        self.body = self.body_handler.create_orb( self, self.scene, pos, 1, FILTER_WEAPON )
        self.body_handler.set_image_at( 'main', 'res/img/weapon/blue_ball.png' )
        return self.body

    def create_projectile( self ) :
        transform = self.apply_spread()
        if ProjectileWeapon.holder_is_player( self ) :
            self.scene.screen.shake_time = 1
        if self.body != 0 :
            if self.get_holder_orbs() == 2 :
                for spread in [-16,16] :
                    angle = math.radians( math.degrees( transform.angle ) + spread )
                    transform = b2Transform( transform.position, b2Rot( angle ) )
                    projectile = Icicle( self.holder.get_owner(), self.scene, transform )
                    self.scene.add_entity( projectile )
                return
            if self.get_holder_orbs() == 3 :
                projectile = IcicleBig( self.holder.get_owner(), self.scene, transform )
                self.scene.add_entity( projectile )
                return
            projectile = Icicle( self.holder.get_owner(), self.scene, transform )
            self.scene.add_entity( projectile )

    def picked( self, owner, slot ) :
        owner.immunities = [ DAMAGE_TYPE_ICE ]
        owner.body_handler.set_image_at( 'head', 'res/img/body/ice_head.png' )
        owner.body_handler.set_image_at( 'right_arm', 'res/img/body/ice_arm.png' )
        owner.body_handler.set_image_at( 'left_arm', 'res/img/body/ice_arm.png' )
        owner.body_handler.set_image_at( 'right_shoulder', 'res/img/body/ice_shoulder.png' )
        owner.body_handler.set_image_at( 'left_shoulder', 'res/img/body/ice_shoulder.png' )
        return SpellOrb.picked( self, owner, slot )

class BoltOrb( SpellOrb ) :

    def __init__( self, scene, pos = ( 0, 0 ) ) :
        SpellOrb.__init__( self, scene, pos, 32, (0.15,0), 3 )
        self.types += [ self.__class__.__name__ ]
        self.firerate_ = 0

    def create_body( self, pos ) :
        ProjectileWeapon.create_body( self )
        self.body = self.body_handler.create_orb( self, self.scene, pos, 1, FILTER_WEAPON )
        self.body_handler.set_image_at( 'main', 'res/img/weapon/white_ball.png' )
        return self.body

    def create_projectile( self ) :
        transform = self.apply_spread()
        if ProjectileWeapon.holder_is_player( self ) :
            self.scene.screen.shake_time = 1
        if self.body != 0 :
            if self.get_holder_orbs() == 2 :
                for spread in [-16,16] :
                    angle = math.radians( math.degrees( transform.angle ) + spread )
                    transform = b2Transform( transform.position, b2Rot( angle ) )
                    projectile = Bolt( self.holder.get_owner(), self.scene, transform )
                    self.scene.add_entity( projectile )
                return
            if self.get_holder_orbs() == 3 :
                projectile = BoltBig( self.holder.get_owner(), self.scene, transform )
                self.scene.add_entity( projectile )
                return
            projectile = Bolt( self.holder.get_owner(), self.scene, transform )
            self.scene.add_entity( projectile )

    def picked( self, owner, slot ) :
        owner.immunities = [ DAMAGE_TYPE_LIGHTNING ]
        owner.body_handler.set_image_at( 'head', 'res/img/body/storm_head.png' )
        owner.body_handler.set_image_at( 'right_arm', 'res/img/body/storm_arm.png' )
        owner.body_handler.set_image_at( 'left_arm', 'res/img/body/storm_arm.png' )
        owner.body_handler.set_image_at( 'right_shoulder', 'res/img/body/storm_shoulder.png' )
        owner.body_handler.set_image_at( 'left_shoulder', 'res/img/body/storm_shoulder.png' )
        return SpellOrb.picked( self, owner, slot )
        
class WhiteOrb( SpellOrb ) :

    def __init__( self, scene, pos = ( 0, 0 ) ) :
        SpellOrb.__init__( self, scene, pos, 32, (0.15,0), 3 )
        self.types += [ self.__class__.__name__ ]
        self.firerate_ = 0

    def create_body( self, pos ) :
        ProjectileWeapon.create_body( self )
        self.body = self.body_handler.create_orb( self, self.scene, pos, 1, FILTER_WEAPON )
        self.body_handler.set_image_at( 'main', 'res/img/weapon/machinegun.png' )
        return self.body

    def create_projectile( self ) :
        transform = self.apply_spread()
        if ProjectileWeapon.holder_is_player( self ) :
            self.scene.screen.shake_time = 1
        if self.body != 0 :
            projectile = Holy( self.holder.get_owner(), self.scene, transform )
            self.scene.add_entity( projectile )

    def picked( self, owner, slot ) :
        owner.immunities = [ DAMAGE_TYPE_PHYSICAL ]
        owner.body_handler.set_image_at( 'head', 'res/img/body/storm_head.png' )
        owner.body_handler.set_image_at( 'right_arm', 'res/img/body/storm_arm.png' )
        owner.body_handler.set_image_at( 'left_arm', 'res/img/body/storm_arm.png' )
        owner.body_handler.set_image_at( 'right_shoulder', 'res/img/body/storm_shoulder.png' )
        owner.body_handler.set_image_at( 'left_shoulder', 'res/img/body/storm_shoulder.png' )
        return SpellOrb.picked( self, owner, slot )

class Projectile( Unit ) :

    def __init__( self, character, scene, origin, offset = -0.8, speed = 800, lifetime = 150 ) :
        pos = origin.position + get_movement_vector( origin.angle, offset )
        Unit.__init__( self, scene, origin.position )
        self.create_body( pos )
        self.character = character
        self.origin = origin
        self.speed = speed * self.body.mass
        self.lifetime = lifetime
        vector = get_movement_vector( origin.angle, -self.speed )
        radians_to_target = get_radians_between_points( (0,0), vector )
        self.body.ApplyForce( vector, self.body.worldCenter, True )
        self.body.transform = [ self.body.transform.position, radians_to_target ]
        self.damage = 1
        #self.body_handler.set_image_at( 'main', 'res/img/effect/default_bullet.png' )
        self.types += [ "projectile" ]

    def update( self, update ) :
        Unit.update( self, update )

    def create_body( self, pos ) :
        self.body = self.body_handler.create_projectile( self, pos, 0.1, FILTER_PROJECTILE )

    def handle_collision( self, my_fixture, colliding_fixture ) :
        collider = colliding_fixture.body.userData.get( 'owner' )
        if "block" in collider.types :
            self.die( collider )
        if "unit" in collider.types :
            self.die( collider )
            self.deal_damage( collider )

    def deal_damage( self, target ) :
        if 'player_character' in target.types and 'player_character' in self.character.types :
            return
        if 'character' in target.types and 'character' in self.character.types :
            return
        if target.take_damage( self, self.damage ) == True :
            pass
            
    def play_sound( self ) :
        self.scene.game.sound_handler.play_sound( self.sound )

class Pellet( Projectile ) :

    def __init__( self, character, scene, origin, offset = -0.8, speed = 500, lifetime = 150 ) :
        Projectile.__init__( self, character, scene, origin, -0.6, 750, 60 )
        self.damage = 1
        self.body_handler.set_image_at( 'main', 'res/img/effect/default_bullet.png' )
        self.types += [ "projectile" ]

    def update( self, update ) :
        Unit.update( self, update )

    def handle_collision( self, my_fixture, colliding_fixture ) :
        collider = colliding_fixture.body.userData.get( 'owner' )
        if "block" in collider.types :
            self.die( collider )
        if "unit" in collider.types :
            self.die( collider )
            self.deal_damage( collider )

    def create_body( self, pos ) :
        self.body = self.body_handler.create_pellet( self, pos, 0.1, FILTER_PROJECTILE )

class SuperBall( Projectile ) :

    def __init__( self, character, scene, origin, offset = -0.8 ) :
        Projectile.__init__( self, character, scene, origin, -0.6, 600, 750 )
        self.damage = Damage( 5, DAMAGE_TYPE_PHYSICAL )
        self.body_handler.set_image_at( 'main', 'res/img/penta/5.png' )
        self.sound = "fire"
        self.play_sound()
        self.types += [ self.__class__.__name__ ]

    def update( self, update ) :
        Unit.update( self, update )

    def handle_collision( self, my_fixture, colliding_fixture ) :
        collider = colliding_fixture.body.userData.get( 'owner' )
        if "block" in collider.types :
            self.die( collider )
        if "unit" in collider.types :
            self.die( collider )
            self.deal_damage( collider )

    def create_body( self, pos ) :
        self.body = self.body_handler.create_pellet( self, pos, 0.1, FILTER_PROJECTILE )

class FireBall( Projectile ) :

    def __init__( self, character, scene, origin, offset = -0.8 ) :
        Projectile.__init__( self, character, scene, origin, -0.6, 600, 750 )
        self.damage = Damage( 5, DAMAGE_TYPE_FIRE )
        self.body_handler.set_image_at( 'main', 'res/img/effect/fireball.png' )
        self.types += [ self.__class__.__name__ ]
        self.sound = "fire"
        self.play_sound()
    
    def update( self, update ) :
        Unit.update( self, update )

    def handle_collision( self, my_fixture, colliding_fixture ) :
        collider = colliding_fixture.body.userData.get( 'owner' )
        if "block" in collider.types :
            self.die( collider )
        if "unit" in collider.types :
            self.die( collider )
            self.deal_damage( collider )

    def create_body( self, pos ) :
        self.body = self.body_handler.create_pellet( self, pos, 0.1, FILTER_PROJECTILE )

class FireBallBig( FireBall ) :

    def __init__( self, character, scene, origin, offset = -0.8 ) :
        FireBall.__init__( self, character, scene, origin, offset )
        self.damage = Damage( 18, DAMAGE_TYPE_FIRE )
        self.body_handler.set_image_at( 'main', 'res/img/effect/fireboom.png' )
        self.sound = "fireboom"
        self.play_sound()

    def create_body( self, pos ) :
        self.body = self.body_handler.create_pellet( self, pos, 0.25, FILTER_PROJECTILE )
        
class Icicle( Projectile ) :

    def __init__( self, character, scene, origin, offset = -0.8 ) :
        Projectile.__init__( self, character, scene, origin, -0.6, 500, 750 )
        self.damage = Damage( 3, DAMAGE_TYPE_ICE )
        self.body_handler.set_image_at( 'main', 'res/img/effect/icebolt.png' )
        self.types += [ self.__class__.__name__ ]
        self.sound = "ice"
        self.play_sound()

    def update( self, update ) :
        Unit.update( self, update )

    def handle_collision( self, my_fixture, colliding_fixture ) :
        collider = colliding_fixture.body.userData.get( 'owner' )
        if "block" in collider.types :
            self.die( collider )
        if "unit" in collider.types :
            self.die( collider )
            self.deal_damage( collider )

    def create_body( self, pos ) :
        self.body = self.body_handler.create_pellet( self, pos, 0.1, FILTER_PROJECTILE )

class IcicleBig( Icicle ) :

    def __init__( self, character, scene, origin, offset = -0.8 ) :
        Icicle.__init__( self, character, scene, origin, offset )
        self.damage = Damage( 10, DAMAGE_TYPE_ICE )
        self.body_handler.set_image_at( 'main', 'res/img/effect/iceshower.png' )
        self.sound = 'icicle'
        self.play_sound()

    def create_body( self, pos ) :
        self.body = self.body_handler.create_pellet( self, pos, 0.25, FILTER_PROJECTILE )
        
class Bolt( Projectile ) :

    def __init__( self, character, scene, origin, offset = -0.8 ) :
        Projectile.__init__( self, character, scene, origin, -0.6, 750, 500 )
        self.damage = Damage( 9, DAMAGE_TYPE_LIGHTNING )
        self.body_handler.set_image_at( 'main', 'res/img/effect/default_bullet.png' )
        self.types += [ self.__class__.__name__ ]
        self.sound = "bolt"
        self.play_sound()

    def update( self, update ) :
        Unit.update( self, update )

    def handle_collision( self, my_fixture, colliding_fixture ) :
        collider = colliding_fixture.body.userData.get( 'owner' )
        if "block" in collider.types :
            self.die( collider )
        if "unit" in collider.types :
            self.die( collider )
            self.deal_damage( collider )

    def create_body( self, pos ) :
        self.body = self.body_handler.create_pellet( self, pos, 0.1, FILTER_PROJECTILE )

class BoltBig( Bolt ) :

    def __init__( self, character, scene, origin, offset = -0.8 ) :
        Bolt.__init__( self, character, scene, origin, offset )
        self.damage = Damage( 30, DAMAGE_TYPE_LIGHTNING )
        self.body_handler.set_image_at( 'main', 'res/img/effect/light_orb.png' )
        self.sound = "bigbolt"
        self.play_sound()
    
    def create_body( self, pos ) :
        self.body = self.body_handler.create_pellet( self, pos, 0.25, FILTER_PROJECTILE )
        
class Holy( Projectile ) :

    def __init__( self, character, scene, origin, offset = -0.8 ) :
        Projectile.__init__( self, character, scene, origin, -0.6, 850, 500 )
        self.damage = Damage( 20, DAMAGE_TYPE_PHYSICAL )
        self.body_handler.set_image_at( 'main', 'res/img/effect/default_bullet.png' )
        self.sound = "holy"
        self.play_sound()
        self.types += [ self.__class__.__name__ ]

    def update( self, update ) :
        Unit.update( self, update )

    def handle_collision( self, my_fixture, colliding_fixture ) :
        collider = colliding_fixture.body.userData.get( 'owner' )
        if "block" in collider.types :
            self.die( collider )
        if "unit" in collider.types :
            self.die( collider )
            self.deal_damage( collider )

    def create_body( self, pos ) :
        self.body = self.body_handler.create_pellet( self, pos, 0.2, FILTER_PROJECTILE )

