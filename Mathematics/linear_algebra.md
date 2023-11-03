## Linear combinations, spans and basis vectors
Linear transformations are matrix transformations that, in two-dimensional space, leave the origin unchanged and do not bend lines.

Span as the set of all points that can be represented as the linear combination of a group of basis vectors.  2 vectors in 2d space span 2d space if they are linearly independent, otherwise their span is a single line.  In 3d space, 2 LI vectors span a plane and 3 span 3d space.

Think of a linear transformation of a span  You can describe it in terms of an operation that you could perform on any vector in the span in order to transform it to its new coordinate.  ...pull from video...

For a transformation in 2D space, we can define a transform as the set of points that our unit vectors become after the transformation.

(0,1) -> (2,1)  and (1,0) -> (-1,0) elegantly represents a transformation, and is often written in the (matrix) form: 

$$\begin{bmatrix}
    2  & -1 \\
    1  & 0 \\
\end{bmatrix}$$
Note that column[i] represents the new coordinate for unit_vec[i]!

## Determinant
Can think of things as ways to SCALE our unit vectors

The determinant of a  transformation (matrix) can be thought of as the magnitude of the change in any given area in the span represented by a transformation.  So a determinant of 2 implies that the area of any region in the space is doubled after the transformation is applied.  The determinant of a 3D matrix represents scaling of the volume of an area.

## Rank, inverses, and null spaces
Rank = Number of dimensions in the output of a transformation

Column space - set of all possible output of $A\vec{v}$

If $Rank(A) < Dim(A)$, then many vectors are mapped to the origin point by transformation $A$.  Otherwise, only 1 vector, the origin itself, is.

The null space, or kernel, of a transformation is the set of all vectors that are mapped to the origin by a transformation

## Non square matrices


# Resources
[Essence of Linear Algebra Youtube series](https://youtu.be/fNk_zzaMoSs?si=MhvkfNweyoKm6NHe)