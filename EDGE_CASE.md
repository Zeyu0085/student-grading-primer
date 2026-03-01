# Document your edge case here
- To get marks for this section you will need to explain to your tutor:
1) The edge case you identified
2) How you have accounted for this in your implementation


## Edge Case: Creating a student without providing `mark`

### Why this is an edge case
In the primer specification, the `POST /students` endpoint states that a student is created with `name`, `course`, and **optionally** `mark`.
However, it does not clearly define what should happen when `mark` is missing:
- Should the request fail?
- Should `mark` be set to a default value?
- Should it be stored as NULL?

### How I handled it
I chose to allow creating a student without `mark` by assigning a **default mark value of `0`**.

### Reasoning
- The spec explicitly says `mark` is optional, so rejecting the request would contradict that.
- A default numeric value keeps the database consistent (the `mark` field is treated as an integer in the system).
- It also allows `/stats` to remain well-defined even when some entries are created without marks.

### Implementation detail
In `POST /students`, I validate that `name` and `course` must be present.
If `mark` is missing, I set it to `0` before calling `db.insert_student(...)`.

This behaviour matches the public automark test `create_student_without_mark_has_mark_field`.

## Edge Case 2: Updating or deleting a non-existing student

### Why this is an edge case

The specification states that:

PUT /students/{id} should return 404 if id does not exist

DELETE /students/{id} should return 404 if student not found

However, it does not specify how the system should detect this condition or what the response should contain.

This creates an edge case when a user attempts to update or delete a student that does not exist in the database.

### How I handled it

Before updating or deleting a student, I first check whether the student exists using:

db.get_student_by_id(student_id)

If the student does not exist, the server returns:

{"error": "student not found"}

with status code 404.

### Reasoning

This ensures the API behaviour matches the specification.

It prevents invalid database operations.

It provides a clear and consistent error response.

### Implementation detail

This logic is implemented in:

    PUT /students/{id}

    DELETE /students/{id}

### Example:
```python
if not student:
    return jsonify({"error": "student not found"}), 404
```