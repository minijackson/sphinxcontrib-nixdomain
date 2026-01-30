{
  stdenvNoCC,
  sphinx,
  python3Packages,
  texliveFull,
}:
stdenvNoCC.mkDerivation {
  pname = "sphinxcontrib-nixdomain-test-root";
  inherit (python3Packages.sphinxcontrib-nixdomain) version;

  src = ./.;

  nativeBuildInputs = [
    sphinx
    python3Packages.myst-parser
    python3Packages.sphinxcontrib-nixdomain
    texliveFull
  ];

  buildPhase = ''
    runHook preBuild
    make html latexpdf
    runHook postBuild
  '';

  installPhase = ''
    runHook preInstall
    mkdir $out
    cp -rav _build/html $out/html
    install -Dt $out/pdf _build/latex/*.pdf
    runHook postInstall
  '';

  env = {
    inherit (python3Packages.sphinxcontrib-nixdomain) NIXDOMAIN_OBJECTS;
  };
}
