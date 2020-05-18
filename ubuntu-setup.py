#!/bin/env python3
import subprocess
import os.path

PROJECTS_PATH = os.path.expanduser('~/projects')
FONTS_PATH = os.path.expanduser('~/.local/share/fonts')
GNOME_SHELL_EXTENSIONS_PATH = os.path.expanduser('~/.local/share/gnome-shell/extensions')

def run(args, cwd=None):
  return subprocess.check_output(args, cwd=cwd)

def is_snap_installed(snap: str):
  try:
    run(['snap', 'list', snap])
    return True
  except:
    return False

def install_snap(snap: str, classic: bool=False, channel: str = None):
  if not is_snap_installed(snap):
    args = ['sudo', 'snap', 'install']
    if classic:
      args.append('--classic')
    if channel is not None:
      args.append('--channel={}'.format(channel))
    args.append(snap)
    is_being_installed(snap)
    run(args)
  else:
    has_been_installed(snap)

def is_pkg_installed(pkg: str):
  try:
    run(['dpkg', '-l', pkg])
    return True
  except:
    return False

def apt_install(pkg: str):
  if not is_pkg_installed(pkg):
    is_being_installed(pkg)
    run(['sudo', 'apt', 'install', '-y', pkg])
  else:
    has_been_installed(pkg)

def create_symlink(link:str, dest:str):
  if not os.path.islink(link):
    run(['ln', '-s', dest, link])

def git_clone(git_url: str, commit: str = None):
  parts = git_url.split('/')
  name_git = parts[-1]
  name = name_git.split('.')[0]

  cloned_dir = os.path.join(PROJECTS_PATH, name)
  if not os.path.isdir(cloned_dir):
    run(['git', 'clone', git_url], cwd=PROJECTS_PATH)

  if commit is not None:
    run(['git', 'checkout', commit], cwd=cloned_dir)

def is_font_installed(font: str):
  fonts = run(['bash', '-c', 'fc-list : family']).decode('utf-8').split('\n')
  return any(font == f for f in fonts)

def is_being_installed(thing: str):
  print('{} is being installed'.format(thing))

def has_been_installed(thing: str):
  print('{} is already installed; skipping'.format(thing))

def install_unite_shell():
  git_clone('https://github.com/hardpixel/unite-shell.git', 'b6b4779c755e0e733ad62412ce8893552101e2b3')
  create_symlink(os.path.join(GNOME_SHELL_EXTENSIONS_PATH, 'unite@hardpixel.eu'), os.path.join(PROJECTS_PATH, 'unite-shell', 'unite@hardpixel.eu'))

def install_font_san_francisco():
  font = 'San Francisco Display'
  if not is_font_installed(font):
    is_being_installed(font)
    git_clone('https://github.com/AppleDesignResources/SanFranciscoFont.git', '59cf0dc3660e99e66813665354f787895fb41fe1')
    run(['bash', '-c', 'mv *.otf {}'.format(FONTS_PATH)], cwd=os.path.join(PROJECTS_PATH, 'SanFranciscoFont'))
    run(['fc-cache', '-v', '-f'])
  else:
    has_been_installed(font)

def create_dir(path: str):
  run(['mkdir', '-p', path])

def main():
  create_dir(PROJECTS_PATH)
  create_dir(GNOME_SHELL_EXTENSIONS_PATH)
  create_dir(FONTS_PATH)

  apt_install('gnome-tweaks')
  apt_install('ubuntu-restricted-extras')
  apt_install('git')

  install_snap('code', classic=True)
  install_snap('node', classic=True, channel='12')
  install_snap('vlc')

  install_unite_shell()
  install_font_san_francisco()


if __name__ == '__main__':
  main()