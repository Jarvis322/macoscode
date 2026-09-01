class Macoscode < Formula
  desc "100 Power-User macOS Tweaks, Interactive TUI Optimizer & CLI Cheatsheet"
  homepage "https://jarvis322.github.io/macoscode/"
  url "https://github.com/Jarvis322/macoscode/archive/refs/heads/main.tar.gz"
  version "2.1.0"
  license "MIT"

  def install
    bin.install "scripts/mc" => "mc"
    bin.install_symlink bin/"mc" => "macoscode"
    pkgshare.install "scripts/macoscode-menubar.swift", "scripts/macoscode.1m.sh"
  end

  test do
    assert_match "macOS", shell_output("#{bin}/mc --help")
  end
end
