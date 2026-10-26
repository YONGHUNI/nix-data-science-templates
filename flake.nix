{
  description = "Editor-independent Nix research and development templates";

  outputs = { self }: {
    templates = {
      python-pixi = {
        path = ./python-pixi;
        description = "Reproducible Python data science with Nix-managed Pixi";
      };

      python-pixi-sapelo2 = {
        path = ./python-pixi-sapelo2;
        description = "Python data science on UGA Sapelo2 HPC with Nix-managed Pixi";
      };

      r-pixi = {
        path = ./r-pixi;
        description = "Reproducible R data science with Nix-managed Pixi";
      };

      latex-nix = {
        path = ./latex-nix;
        description = "Reproducible XeLaTeX, latexmk and tex-fmt with Nix";
      };

      default = self.templates.python-pixi;
    };
  };
}
