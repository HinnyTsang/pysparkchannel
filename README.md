# pysparkchannel

## Usage

Tools to move module to spark cluster.

---

## Example

See [example notebook](./example/example.ipynb).

---

## Installation

Go to your project directory and run the following command

### 1. If svn installed

Run

```bash
svn checkout https://github.com/HinnyTsang/pysparkchannel/tree/main/pysparkchannesl
```

### 2. Only git installed

Run

```bash
git init

git remote add pysparkchannel https://github.com/HinnyTsang/pysparkchannel.git

git config core.sparseCheckout true

echo "pysparkchannel" > .git/info/sparse-checkout

git pull pysparkchannel main
```

---

## Update

```bash
rm -rf pysparkchannel
git pull pysparkchannel main
```
