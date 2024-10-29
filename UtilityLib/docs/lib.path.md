# Module UtilityLib.lib.path:

class EntityPath(pathlib.Path)
  EntityPath(*args, **kwargs)

  A versatile extension of Python's built-in `Path` class to simplify and enhance file and directory handling.

  Key Features:
  --------------
  1. **Extended Operators**: Implements custom operators (`//`, `%`, `-`, `+`) for intuitive path manipulation.
      - `//` (Floor division): Splits the path into segments based on integer or string input.
      - `%` (Modulo): Allows dynamic string formatting within paths.
      - `-` (Subtraction): Removes segments from the path, either by an index or up to a matching string.
      - `+` (Addition): Concatenates new path components easily.

  2. **Search and Match**: Provides methods for pattern matching and file type identification.
      - Methods like `search`, `has`, and `get_match` allow users to quickly find files or directories using flexible patterns.

  3. **File and Directory Operations**: Simplifies common filesystem tasks like reading, writing, moving, copying, and deleting files or directories.
      - Methods for safely deleting files (`delete` with `force_delete`).
      - List all files, directories, or both using `list_files`, `list_dirs`, or `list_items`.
      - Quick read/write utilities like `read_text`, `write_text`, `head`, and `tail` for file content manipulation.

  4. **Metadata and Stats**: Efficiently retrieve file or directory metadata.
      - Properties like `size`, `permission`, `created`, `updated`, and `hash` provide quick access to key attributes.
      - Comprehensive stat retrieval via `stats` for access, modification, and creation times.

  5. **Compression Detection**: Automatically detect if a file is compressed, based on file extension (`is_gz`).

  6. **Path Formatting**: Methods like `rel_path`, `parent`, and `full_path` make it easy to convert paths to relative, parent, or absolute forms.

  Additional Utilities:
  ---------------------
  - `validate`: Creates the file or directory if it doesn't exist.
  - `move` and `copy`: Move or copy files and directories to new locations with automatic parent directory creation if necessary.
  - `get_hash`: Calculate file or directory hash using common algorithms like `sha256` and `md5` for integrity checks.

  This class is designed to make filesystem operations more intuitive and reduce repetitive boilerplate code, improving readability and efficiency in path manipulation tasks.

  ## MRO
      EntityPath
      pathlib.Path
      pathlib.PurePath
      builtins.object

  ## Methods

  __add__(self, what='')

  __floordiv__(self, what)
      Flood Division (// operator) to return based on str or int

  __len__ = len(self)

  __mod__(self, what='')
      Modulo operand operation on EntityPath

  __str__(self)
      Return the string representation of the path, suitable for
      passing to system calls.

  __sub__(self, what)
      Subtraction operator (-) for removing segments from a path.

  contains = has(self, file=None)

  copy(self, destination)
      Copy the file or directory to a new location.

  delete(self, force_delete=None)

  exists(self)
      Check if the path exists.

  ext_type = search(self, pattern='**')

  file_type = search(self, pattern='**')

  folders = list_dirs(self)

  get_hash(self, algorithm='sha256')
      Compute the hash of the file or directory using the specified algorithm.

      :param algorithm: Hash algorithm to use ('md5', 'sha256', etc.)
      :return: The computed hash as a hexadecimal string

  get_match(self, pattern='*txt')

  get_name(self)
      Return the name of the file or directory.

  get_size(self, converter=None)
      Return the size of the file or directory.

  get_stats(self)

  get_stem(self)
      Return the stem of the file or directory (filename without extension).

  has(self, file=None)
      Case sensitive check if pattern (e.g., **/file.txt; *ile.tx*) exists

  has_dir = has(self, file=None)

  has_file = has(self, file=None)

  head(self, lines=1)
      Return first few lines of a file

  help(self)

  len(self)

  list_dirs(self)
      List all directories in the directory.

  list_files(self, relative=True)
      List all files in the directory.

  list_items(self)
      List all items (files and directories) in the directory.

  lower(self)

  move(self, destination)
      Move the file or directory to a new location.

  parent(self, level=0)
      Return the parent directory.

  read = _read_file(self, method=None)

  read_lines = _read_lines(self, num_lines=None)

  read_text = _read_file(self, method=None)

  readline = _read_lines(self, num_lines=None)

  readlines = _read_lines(self, num_lines=None)

  rel_path(self, _path=None)
      Return the relative path from the current working directory.

  search(self, pattern='**')

  tail(self, lines=1, buffer_size=4098)
      Tail a file and get X lines from the end
      Source: https://stackoverflow.com/a/13790289

  type_ext = search(self, pattern='**')

  upper(self)

  validate(self)
      Make directory/file if doesn't exist.

  write = write_text(self, data, mode='a')

  write_text(self, data, mode='a')
      Write the given text to the file.

  ----------------------------------------------------------------------
  Static methods defined here:

  __new__(self, *args, **kwargs)
      Construct a PurePath from one or several strings and or existing
      PurePath objects.  The strings and path objects are combined so as
      to yield a canonicalized path, which is incorporated into the
      new PurePath object.

  ----------------------------------------------------------------------
  ## ReadOnlyProperties

  accessed

  created

  dirs

  entities

  ext

  files

  full_path
      Return the absolute path.

  hash

  is_compressed

  is_gz

  items

  mode

  modified

  permission

  size

  stats

  text

  updated
