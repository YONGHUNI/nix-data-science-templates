{
  description = "Nix data science project templates";

  outputs = { self }: {
    templates = {
      python-conda = {
        path = ./python-conda;
        description = "Python data science with Nix + micromamba + conda-lock";
      };

      python-nix = {
        path = ./python-nix;
        description = "Pure Nix Python data science environment";
      };

      r-renv = {
        path = ./r-renv;
        description = "R data science with Nix + renv";
      };

      r-nix = {
        path = ./r-nix;
        description = "Pure Nix R data science environment";
      };

      default = self.templates.python-conda;
    };
  };
}
