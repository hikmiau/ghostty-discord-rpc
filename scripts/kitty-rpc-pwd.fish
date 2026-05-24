function __kitty_rpc_pwd --on-variable PWD
    mkdir -p ~/.cache
    echo $PWD > ~/.cache/kitty-rpc-pwd
end

mkdir -p ~/.cache
echo $PWD > ~/.cache/kitty-rpc-pwd
