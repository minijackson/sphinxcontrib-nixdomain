{
  stdenvNoCC,
  lib,
  python3,
  nixdomainObjects,
}:
stdenvNoCC.mkDerivation {
  pname = "my-project-docs";
  version = "0.0.1-beta2";

  src = ../docs;

  nativeBuildInputs = with python3.pkgs; [
    myst-parser
    sphinx
    sphinx-design
    sphinxcontrib-nixdomain
  ];

  dontConfigure = true;

  buildPhase = ''
    runHook preBuild
    make html
    runHook postBuild
  '';

  installPhase = ''
    runHook preInstall
    mkdir -p $out/share/doc/my-project/
    cp -r _build/html $out/share/doc/my-project/
    runHook postInstall
  '';

  env.NIXDOMAIN_OBJECTS = nixdomainObjects;

  meta = {
    description = "My super documentation";
    # ...
  };
}
