{
  enterShell = ''
    echo "Please set the environment variable API_KEY manually for now."
  '';
  languages.python = {
    enable = true;
    venv = {
      enable = true;
      requirements = builtins.readFile ./requirements.txt;
    };
  };
}
