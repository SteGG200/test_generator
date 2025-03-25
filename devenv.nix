{pkgs, ...}: {
  dotenv.enable = true;
  languages.python = {
    enable = true;
    package = pkgs.python39;
    venv = {
      enable = true;
      requirements = builtins.readFile ./requirements.txt;
    };
  };
}
