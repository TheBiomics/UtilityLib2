class FileSystemUtility(UtilityLib.core.db.DatabaseUtility)
  FileSystemUtility(*args, **kwargs)

  ## MRO:
      FileSystemUtility
      UtilityLib.core.db.DatabaseUtility
      UtilityLib.core.cmd.CommandUtility
      UtilityLib.core.log.LoggingUtility
      UtilityLib.core.time.TimeUtility
      UtilityLib.BaseUtility
      builtins.object

  ## Methods:

  __init__(self, *args, **kwargs)

  add_tgz_files = _add_files_to_tar_gzip(self, *args, **kwargs)

  backup = _backup_file(self, *args, **kwargs)

  backup_file = _backup_file(self, *args, **kwargs)

  change_ext(self, *args, **kwargs)

  check_path(self, *args, **kwargs)
      Checks if path(s) exists or not

      @param
      0|path: String, path, or list of paths

      @return boolean
      True|False

  compress_dir = _compress_dir(self, *args, **kwargs)

  compress_gz = _compress_file_to_gzip(self, *args, **kwargs)

  compress_to_gzip = _compress_file_to_gzip(self, *args, **kwargs)

  compress_zip = _compress_dir(self, *args, **kwargs)

  conv_xml_to_dict = xml_to_dict(self, *args, **kwargs)

  convert_bytes(self, *args, **kwargs)
      Converts bytes to ("B", "KiB", "MiB", "GiB", "TiB", "PiB", "EiB", "ZiB", "YiB")... etc

      :params _bytes|0: float

  convert_xml_to_dict = xml_to_dict(self, *args, **kwargs)

  copy = _copy_from_to(self, *args, **kwargs)

  copy_file = _copy_from_to(self, *args, **kwargs)

  copy_to = _copy_from_to(self, *args, **kwargs)

  count_file_lines(self, *args, **kwargs)
      Quickly counts lines in a file or gz file
      @stats: counts lines in a 7GB gz file in 2min

  create_copy = _copy_from_to(self, *args, **kwargs)

  create_dir(self, *args, **kwargs) -> dict

  create_file_backup = _backup_file(self, *args, **kwargs)

  delete_file = delete_path(self, *args, **kwargs)

  delete_files(self, *args, **kwargs)
      Deletes multiple files or paths

  delete_path(self, *args, **kwargs)
      Deletes a file or directory

      @params
      0|path (str): File path
      1|flag_files_only (boolean): To keep directory structure but delete all the files

      @ToDo:
      Instead of deletion, move the entity to temporary directory to avoid any accidental loss of data

  dict_to_csv(self, *args, **kwargs)

  dir_details = _dir_file_inventory(self, *args, **kwargs)

  dir_exists = check_path(self, *args, **kwargs)

  download_content(self, *args, **kwargs)

  exists = check_path(self, *args, **kwargs)

  ext = file_ext(self, *args, **kwargs)

  ext_files = _walk_files_by_extension(self, *args, **kwargs)

  extract_zip = _uncompress_archive(self, *args, **kwargs)

  file_dir(self, *args, **kwargs)
      Returns parent directory path from the filepath

  file_exists = check_path(self, *args, **kwargs)

  file_ext(self, *args, **kwargs)
      Returns file fxtension

      @params
      0|file_path
      1|num_ext=1: Number of extension with a dot

  file_extension = file_ext(self, *args, **kwargs)

  file_name = filename(self, *args, **kwargs)

  file_stats = _dir_file_inventory(self, *args, **kwargs)

  filename(self, *args, **kwargs)
      @function
      Returns file_name from path <path>/<file_name>.<extn>.<ext2>.<ext1>

      @params
      0|file_path
      1|with_ext=default False
      2|with_dir=default False
      3|num_ext=default 1 or -1 to guess extensions

      @ToDo
      num_ext=-1 to guess extensions

  find_dirs = _search_dir_filter(self, *args, **kwargs)

  find_file_types = _walk_files_by_extension(self, *args, **kwargs)

  find_files = _search_file_filter(self, *args, **kwargs)

  from_JSON = read_json(self, *args, **kwargs)

  from_html = read_html(self, *args, **kwargs)

  from_json = read_json(self, *args, **kwargs)

  from_text = read_text(self, *args, **kwargs)

  get_existing(self, *args, **kwargs)
      Returns first existing path from the given list

      @extends check_path

  get_ext = file_ext(self, *args, **kwargs)

  get_extension = file_ext(self, *args, **kwargs)

  get_file(self, *args, **kwargs)
      @function
      downloads a url content and returns content of the file
      uses urlretrieve as fallback

      @params
      :param url|0: (str)
      :param destination|1: (None|str|path)
      :param return_text|2: (bool)
      :param overwrite|3: (False|bool)= forces to download the content if file already exists
      :param form_values|4: (None|dict)= values to be submitted while downloading file from url USING GET METHOD
      :param headers|5: headers to set for downloading files
      :param method|6: ("get"|"post")= method of downloading file

      @returns
      :return: bool

  get_file_backup(self, *args, **kwargs)
      Get latest file backup

  get_file_backups(self, *args, **kwargs)

  get_file_content(self, *args, **kwargs)
      @extends get_file

      @function
      returns content of a file

  get_file_size(self, *args, **kwargs)
      Returns file size(s)

      :params file_path|0: string or iterable

      :returns: [(file_path, file_size, size_unit), ]

  get_file_types = _walk_files_by_extension(self, *args, **kwargs)

  get_item_details = _dir_file_inventory(self, *args, **kwargs)

  get_open_file_descriptors(self, *args, **kwargs)

  get_pickle = read_pickle(self, *args, **kwargs)

  gz = _compress_file_to_gzip(self, *args, **kwargs)

  gzip = _compress_file_to_gzip(self, *args, **kwargs)

  html = read_html(self, *args, **kwargs)

  list_tgz_files(self, *args, **kwargs)

  list_tgz_items(self, *args, **kwargs)
      @bug: Doesn't renew file in loop due to path_tgz
      Workaround to assign path_tgz at the beginning of every loop.

  list_zip_files(self, *args, **kwargs)

  list_zip_items(self, *args, **kwargs)

  move(self, *args, **kwargs)
      Copies source and deletes using .delete_path

  parse_html(self, *args, **kwargs)

  parse_jsonl_gz(self, *args, **kwargs)

  parse_latex(self, *args, **kwargs)

  path_exists = check_path(self, *args, **kwargs)

  pickle = write_pickle(self, *args, **kwargs)

  pkl = write_pickle(self, *args, **kwargs)

  read(self, *args, **kwargs)
      @ToDo:
      - Guess type of file and return type based on the path, extension with exceptions
      @Temporarily resolves to read_text

  read_gz_file(self, *args, **kwargs)
      Reads gzipped files only (not tar.gz, tgz or a compressed file) line by line (fasta, txt, jsonl, csv, and tsv etc...)
      Can advance the counter to skip set of lines

  read_html(self, *args, **kwargs)

  read_json(self, *args, **kwargs)

  read_pickle(self, *args, **kwargs)
      @function
      reads pickle file

      @params
      0|source (str|path): File path
      1|default (any): default value to return if file not found
      2|flag_compressed (boolean): If file is gz compressed (other compressions are not implemented)

      @return
      None: if some error occurs
      python object after reading the pkl file

  read_text(self, *args, **kwargs)
      @ToDo
        * implement yield|generator to handle larger files
        * check if file extension is gz, try reading it as gz
        * `str.splitlines(keepends=False)`

  read_tgz_file(self, *args, **kwargs)

  read_xml(self, *args, **kwargs)

  read_zipfile(self, *args, **kwargs)

  rename(self, *args, **kwargs)

  save_json = write_json(self, *args, **kwargs)

  save_pickle = write_pickle(self, *args, **kwargs)

  save_xml = write_xml(self, *args, **kwargs)

  search = _search_file_filter(self, *args, **kwargs)

  search_dirs = _search_dir_filter(self, *args, **kwargs)

  search_file_types = _walk_files_by_extension(self, *args, **kwargs)

  search_files = _search_file_filter(self, *args, **kwargs)

  split_file(self, *args, **kwargs)
      WIP: Split file in smaller files

  text = read_text(self, *args, **kwargs)

  tgz = _compress_dir_to_tgz(self, *args, **kwargs)

  to_gz = _compress_file_to_gzip(self, *args, **kwargs)

  to_pickle = write_pickle(self, *args, **kwargs)

  to_pkl = write_pickle(self, *args, **kwargs)

  to_tgz = _compress_dir_to_tgz(self, *args, **kwargs)

  uncompress = _uncompress_archive(self, *args, **kwargs)

  unpickle = read_pickle(self, *args, **kwargs)

  unzip = _uncompress_archive(self, *args, **kwargs)

  validate_dir(self, *args, **kwargs)

  validate_path = validate_dir(self, *args, **kwargs)

  validate_subdir(self, *args, **kwargs)

  write(self, *args, **kwargs)
      @params
        0|destination:
        1|content
        2|append (boolean)
        3|encoding
        4|mode
        5|position: Write position by moving cursor

      @return
        check_path(destination)

  write_json(self, *args, **kwargs)
      @function
      Writes dict content as JSON

      @returns
      True|False if file path exists

  write_pickle(self, *args, **kwargs)
      @function
      Writes python object as pickle file

      @params
      0|destination (str|path)
      1|content (any): Python object for pickling

      @returns
      True|False if file path exists

      @update
        Uses GZip for compression
        File extension pkl.gz used against df.gz|pd.gz pickled files

  write_xml(self, *args, **kwargs)
      @function
      Writes XML string to file

      @returns
      True|False if file path exists

  xml_to_dict(self, *args, **kwargs)
      Converts XML to dict

      @returns
      dict of the converted xml

  zip(self, *args, **kwargs)
