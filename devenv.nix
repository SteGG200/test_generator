{pkgs, ...}: {
  dotenv.enable = true;

  env.LD_LIBRARY_PATH = pkgs.lib.makeLibraryPath [
    pkgs.stdenv.cc.cc.lib
    pkgs.zlib
  ];

  languages.python = {
    enable = true;
    package = pkgs.python39;
    venv = {
      enable = true;
      requirements = builtins.readFile ./requirements.txt;
    };
  };

  packages = [
    pkgs.pandoc
    pkgs.wkhtmltopdf
  ];
}
