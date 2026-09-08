package goroutines

import (
	"reflect"
	"testing"
)

func TestSquares(t *testing.T) {
	got := Squares([]int{1, 2, 3, 4, 5})
	want := []int{1, 4, 9, 16, 25}
	if !reflect.DeepEqual(got, want) {
		t.Fatalf("Squares(...) = %v; want %v", got, want)
	}
}

func TestSquaresPreservesOrderAtScale(t *testing.T) {
	nums := make([]int, 500)
	want := make([]int, 500)
	for i := range nums {
		nums[i] = i
		want[i] = i * i
	}
	got := Squares(nums)
	if !reflect.DeepEqual(got, want) {
		t.Fatalf("Squares at scale did not preserve input order -- " +
			"check that each goroutine writes result[i], not some shared/reused index")
	}
}

func TestSquaresEmpty(t *testing.T) {
	got := Squares(nil)
	if len(got) != 0 {
		t.Fatalf("Squares(nil) = %v; want empty", got)
	}
}
