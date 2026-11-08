package main

import (
	"bytes"
	"encoding/csv"
	"testing"
)

func TestExportar(t *testing.T) {
	var b bytes.Buffer
	if err := exportar([]Registro{{"2026-10-01", "10.00"}}, csv.NewWriter(&b)); err != nil {
		t.Fatal(err)
	}
	if b.String() != "2026-10-01,10.00\n" {
		t.Fatalf("saída inesperada: %q", b.String())
	}
}
