package main

import (
	"encoding/csv"
	"flag"
	"fmt"
	"os"
)

type Registro struct {
	Data  string
	Valor string
}

func exportar(regs []Registro, w *csv.Writer) error {
	for _, r := range regs {
		if err := w.Write([]string{r.Data, r.Valor}); err != nil {
			return err
		}
	}
	w.Flush()
	return w.Error()
}

func main() {
	saida := flag.String("saida", "export.csv", "arquivo de saída")
	flag.Parse()
	f, err := os.Create(*saida)
	if err != nil {
		fmt.Fprintln(os.Stderr, err)
		os.Exit(1)
	}
	defer f.Close()
	regs := []Registro{{"2026-10-01", "10.00"}, {"2026-11-02", "5.50"}}
	if err := exportar(regs, csv.NewWriter(f)); err != nil {
		fmt.Fprintln(os.Stderr, err)
		os.Exit(1)
	}
}
