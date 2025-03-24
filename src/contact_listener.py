"""
contact_listener.py

This module contains the ContactListener class, which handles collision events
in the Box2D world.

The ContactListener class is responsible for:
- Detecting when the player lands on or leaves a platform.
- Enabling one-way collision behavior for platforms (pass-through from below).

Dependencies:
- Box2D: Used for physics simulation.
- Player: The player object that interacts with platforms.

Author:     DevXCVIII
Date:       March 24, 2025
"""

import Box2D

class ContactListener(Box2D.b2.contactListener):
    """
    Handles collision events in the Box2D world.

    This class is used to:
    - Detect when the player lands on or leaves a platform.
    - Enable one-way collision behavior for platforms, allowing the player to
      pass through from below but land on them from above.

    Methods:
        BeginContact(contact):
            Called when two fixtures begin to touch. Sets the player as grounded
            if they land on a platform.
        EndContact(contact):
            Called when two fixtures cease to touch. Sets the player as not
            grounded when they leave a platform.
        PreSolve(contact, old_manifold):
            Called before the physics engine resolves a collision. Disables
            collision if the player is below a platform, enabling one-way behavior.
    """

    def __init__(self, player):
        super().__init__()
        self.player = player

    def _get_other_fixture(self, contact):
        """
        Helper method to get the fixture that is not the player's body.

        Args:
            contact: The Box2D contact object.

        Returns:
            The fixture that is not the player's body, or None if the player
            is not involved in the collision.
        """
        player_body = self.player.body
        fixture_a = contact.fixtureA
        fixture_b = contact.fixtureB

        if fixture_a.body == player_body:
            return fixture_b
        elif fixture_b.body == player_body:
            return fixture_a
        return None

    def BeginContact(self, contact):
        """
        Called when two fixtures begin to touch.
        Sets the player as grounded if they land on a platform.
        """
        other_fixture = self._get_other_fixture(contact)
        if other_fixture and other_fixture.body.userData == "platform":
            self.player.grounded = True

    def EndContact(self, contact):
        """
        Called when two fixtures cease to touch.
        Sets the player as not grounded when they leave a platform.
        """
        other_fixture = self._get_other_fixture(contact)
        if other_fixture and other_fixture.body.userData == "platform":
            self.player.grounded = False

    def PreSolve(self, contact, old_manifold):
        """
        Called before the physics engine resolves a collision.

        This method is used to enable one-way collision behavior for platforms.
        If the player is below a platform, the collision is disabled, allowing
        the player to pass through. If the player is above the platform, the
        collision remains enabled, allowing the player to land on it.

        Args:
            contact: The Box2D contact object representing the collision.
            old_manifold: The previous collision manifold (not used here).
        """
        other_fixture = self._get_other_fixture(contact)
        if other_fixture and other_fixture.body.userData == "platform":
            platform_y = other_fixture.body.position.y
            player_y = self.player.body.position.y
            if player_y < platform_y:
                contact.enabled = False