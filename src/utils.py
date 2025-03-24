def blit_text_with_anchor(screen, text_surface, anchor, offset=(0, 0)):
    """
    Draws a text surface on the screen using an anchor point.

    Args:
        screen: The Pygame screen to draw on.
        text_surface: The rendered text surface.
        anchor: A tuple (x, y) where x and y are between 0 and 1 (e.g., (0.5, 0.5) for center).
        offset: A tuple (x_offset, y_offset) to adjust the position.
    """
    screen_width, screen_height = screen.get_size()
    text_width, text_height = text_surface.get_size()

    # Calculate position based on anchor
    x = screen_width * anchor[0] - text_width * anchor[0] + offset[0]
    y = screen_height * anchor[1] - text_height * anchor[1] + offset[1]

    # Draw the text
    screen.blit(text_surface, (x, y))