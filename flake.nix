{
  description = "Positron-focused Nix data science project templates";

  outputs = { self }: {
    templates = {
      python-pixi = {
        path = ./python-pixi;
        description = "Python data science for Positron with Nix-managed Pixi";
      };

      r-pixi = {
        path = ./r-pixi;
        description = "R data science for Positron with Nix-managed Pixi";
      };

      default = self.templates.python-pixi;
    };
  };
}
