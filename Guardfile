# Execute shell commands on file change.
guard :shell  do
  # On any change within the input directory, regenerate site and show
  # notification.
  watch %r{^input_dir} do |m|
    `python generate_comic_page.py`
    n m[0] + " was changed", "Regenerating site", :success
  end
end
