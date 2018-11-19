"""Assignment 2: Treemap Visualiser

=== CSC148 Fall 2016 ===
Diane Horton and David Liu
Department of Computer Science,
University of Toronto

=== Module Description ===
This module contains the code to run the treemap visualisation program.
It is responsible for initializing an instance of AbstractTree (using a
concrete subclass, of course), rendering it to the user using pygame,
and detecting user events like mouse clicks and key presses and responding
to them.
"""
import pygame
from tree_data import FileSystemTree
from population import PopulationTree
import os
import sys


# Screen dimensions and coordinates
ORIGIN = (0, 0)
WIDTH = 1024
HEIGHT = 600  # 768
FONT_HEIGHT = 30                       # The height of the text display.
TREEMAP_HEIGHT = HEIGHT - FONT_HEIGHT  # The height of the treemap display.

# Font to use for the treemap program.
FONT_FAMILY = 'Consolas'


def run_visualisation(tree):
    """Display an interactive graphical display of the given tree's treemap.

    @type tree: AbstractTree
    @rtype: None
    """
    # Setup pygame
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, 1000))

    # Render the initial display of the static treemap.
    render_display(screen, tree, '')

    # Start an event loop to respond to events.
    event_loop(screen, tree)


def render_display(screen, tree, text):
    """Render a treemap and text display to the given screen.

    Use the constants TREEMAP_HEIGHT and FONT_HEIGHT to divide the
    screen vertically into the treemap and text comments.

    @type screen: pygame.Surface
    @type tree: AbstractTree
    @type text: str
        The text to render.
    @rtype: None
    """
    # First, clear the screen
    pygame.draw.rect(screen, pygame.color.THECOLORS['black'],
                     (0, 0, WIDTH, HEIGHT))
    rect_list = tree.generate_treemap((0, 0, WIDTH, TREEMAP_HEIGHT))
    for rect in rect_list:
        if rect[0][2] == 0 or rect[0][3] == 0:
            rect_list.remove(rect)

    for element in rect_list:
        pygame.draw.rect(screen, element[1], element[0])

    _render_text(screen, text)

    # This must be called *after* all other pygame functions have run.
    pygame.display.flip()


def _render_text(screen, text):
    """Render text at the bottom of the display.

    @type screen: pygame.Surface
    @type text: str
    @rtype: None
    """
    assert text is not None, 'Text is None!'
    # The font we want to use
    font = pygame.font.SysFont(FONT_FAMILY, FONT_HEIGHT - 8)
    text_surface = font.render(text, 1, pygame.color.THECOLORS['white'])

    # Where to render the text_surface
    text_pos = (0, HEIGHT - FONT_HEIGHT + 4)
    screen.blit(text_surface, text_pos)


def event_loop(screen, tree):
    """Respond to events (mouse clicks, key presses) and update the display.

    Note that the event loop is an *infinite loop*: it continually waits for
    the next event, determines the event's type, and then updates the state
    of the visualisation or the tree itself, updating the display if necessary.
    This loop ends when the user closes the window.

    @type screen: pygame.Surface
    @type tree: AbstractTree
    @rtype: None
    """
    selected_leaf = None
    selected_leaf_text = ''
    treemap = tree.generate_treemap((0, 0, WIDTH, HEIGHT))

    while True:
        # Wait for an event
        event = pygame.event.poll()
        if event.type == pygame.QUIT:
            return

        if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            location = event.pos
            if location[1] <= TREEMAP_HEIGHT:
                text, selected_leaf = tree.get_text(location, treemap)
                selected_leaf_text = text
                render_display(screen, tree, text)
        elif event.type == pygame.MOUSEBUTTONUP and event.button == 3:
            location = event.pos
            if location[1] <= TREEMAP_HEIGHT:
                new_tree = tree.remove_leaf(location, treemap)
                render_display(screen, new_tree, '')
        elif selected_leaf is not None and event.type == pygame.KEYUP and \
                event.key == pygame.K_UP:
            new_tree = tree.change_leaf_size(selected_leaf, True)
            new_text = selected_leaf_text.split('(', 1)[0]
            new_text += '(' + str(selected_leaf.data_size) + ')'
            render_display(screen, new_tree, new_text)
        elif selected_leaf is not None and event.type == pygame.KEYUP and \
                event.key == pygame.K_DOWN:
            new_tree = tree.change_leaf_size(selected_leaf, False)
            new_text = selected_leaf_text.split('(', 1)[0]
            new_text += '(' + str(selected_leaf.data_size) + ')'
            render_display(screen, new_tree, new_text)


def run_treemap_file_system(path):
    """Run a treemap visualisation for the given path's file structure.

    Precondition: <path> is a valid path to a file or folder.

    @type path: str
    @rtype: None
    """
    file_tree = FileSystemTree(path)
    run_visualisation(file_tree)


def run_treemap_population():
    """Run a treemap visualisation for World Bank population data.

    @rtype: None
    """
    pop_tree = PopulationTree(True)
    run_visualisation(pop_tree)


if __name__ == '__main__':
    # Uncomment the following 2 lines to run PythonTA, which runs a few tests.
    # import python_ta
    # python_ta.check_all(config='pylintrc.txt')

    if len(sys.argv) < 2 or sys.argv[1] not in ['population', 'filesystem']:
        print('Usage: python {} [population|filesystem]'.format(sys.argv[0]))
        exit(1)
    elif sys.argv[1] == 'filesystem':
        # Runs the file system treemap on the parent directory of your working directory.
        run_treemap_file_system(os.path.abspath(os.path.join(os.getcwd(), os.pardir)))
    else:
        run_treemap_population()
