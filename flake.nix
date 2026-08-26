{
  description = "Nix data science project templates";

  outputs = { self }: {
    templates = {
      python-conda = {
        path = ./python-conda;
        description = "Python data science with Nix-managed micromamba";
      };

      python-pixi = {
        path = ./python-pixi;
        description = "Python data science with Nix-managed Pixi";
      };

      python-nix = {
        path = ./python-nix;
        description = "Pure Nix Python data science environment";
      };

      r-pixi = {
        path = ./r-pixi;
        description = "R data science with Nix-managed Pixi";
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
