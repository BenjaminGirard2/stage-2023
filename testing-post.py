from postprocessing import PostProcessing

filename = r'C:\Users\Benjamin\Desktop\stage 2023\vtk-files\al_test_1.vtk'
post = PostProcessing(filename)


post.filter_coords_in_z()
post.filter_coords_in_x(3, -5)
post.filter_coords_in_y(0.1)
post.apply_flat_polishing(0.1)
post.plot_displacement()
