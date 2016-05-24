import os
import subprocess


from argparse import ArgumentParser


def _get_mapping_file(name):
    url = "https://raw.githubusercontent.com/dpryan79/ChromosomeMappings/master/%s.txt" % args.name
    out_put = "%s.txt" % name
    if os.path.exists(out_put):
        return out_put
    else:
        cmd = "wget -N -c -O {out_put} {url}".format(**locals())
        print cmd
        subprocess.check_call(cmd.split())
        return out_put

if __name__ == "__main__":
    parser = ArgumentParser(description="map chromosomes from ensembl <=> ucsc <=> gencode")
    parser.add_argument("--name", help="chomosome mapping file name", required=1)
    parser.add_argument("--rev", help="reverse mapping", action="store_true")
    parser.add_argument("--input", help="input file with frist column being chromosome", required=1)
    parser.add_argument("--out", help="output file name", required=1)

    args = parser.parse_args()

    mapping_file = _get_mapping_file(args.name)
    m = dict()
    with open(mapping_file) as in_handle:
        for line in in_handle:
            if len(line.split()) > 1:
                c_orig, c_final = line.strip().split()
                if args.rev:
                    c_final, c_orig = line.strip().split()
                m[c_orig] = c_final

    with open(args.input) as in_handle:
        with open(args.out, 'w') as out_handle:
            for line in in_handle:
                cols = line.strip().split()
                if cols[0] in m:
                    cols[0] = m[cols[0]]
                    print >>out_handle, "\t".join(cols)
