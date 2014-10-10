package com.example.lhm_capstone;

import android.app.Activity;
import android.net.Uri;
import android.os.Bundle;
import android.app.Fragment;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.view.ViewGroup.LayoutParams;
import android.widget.Button;
import android.widget.EditText;
import android.widget.LinearLayout;
import android.widget.TextView;
import android.widget.Toast;
import android.widget.PopupWindow;

/**
 * A simple {@link android.support.v4.app.Fragment} subclass. Activities that
 * contain this fragment must implement the
 * {@link InventorySearchFragment.OnFragmentInteractionListener} interface to
 * handle interaction events. Use the
 * {@link InventorySearchFragment#newInstance} factory method to create an
 * instance of this fragment.
 * 
 */
public class InventorySearchFragment extends Fragment implements android.view.View.OnClickListener {
	// TODO: Rename parameter arguments, choose names that match
	// the fragment initialization parameters, e.g. ARG_ITEM_NUMBER
	private static final String ARG_PARAM1 = "param1";
	private static final String ARG_PARAM2 = "param2";

	// TODO: Rename and change types of parameters
	private String mParam1;
	private String mParam2;

	InventorySearchFragmentInteractionListener mListener;
	
	private EditText vinTextfield;
	LinearLayout layoutOfPopup;
	PopupWindow popup;
	TextView popupText;
	
	Button applyFilterButton;
	
	/**
	 * Use this factory method to create a new instance of this fragment using
	 * the provided parameters.
	 * 
	 * @param param1
	 *            Parameter 1.
	 * @param param2
	 *            Parameter 2.
	 * @return A new instance of fragment InventorySearchFragment.
	 */
	// TODO: Rename and change types and number of parameters
	public static InventorySearchFragment newInstance(String param1,
			String param2) {
		InventorySearchFragment fragment = new InventorySearchFragment();
		Bundle args = new Bundle();
		args.putString(ARG_PARAM1, param1);
		args.putString(ARG_PARAM2, param2);
		fragment.setArguments(args);
		return fragment;
	}

	public InventorySearchFragment() {
		// Required empty public constructor
	}

	@Override
	public void onCreate(Bundle savedInstanceState) {
		super.onCreate(savedInstanceState);
		//vinTextfield = (EditText) findViewById(R.id.editText1);
		init();
		popupInit();
		if (getArguments() != null) {
			mParam1 = getArguments().getString(ARG_PARAM1);
			mParam2 = getArguments().getString(ARG_PARAM2);
		}
	}

	private EditText findViewById(int edittext1) {
		// TODO Auto-generated method stub
		return null;
	}

	@Override
	public View onCreateView(LayoutInflater inflater, ViewGroup container,
			Bundle savedInstanceState) {
		// Set onClickListener to the go_button
		View view = inflater.inflate(R.layout.fragment_inventory_search, container, false);
		applyFilterButton = (Button) view.findViewById(R.id.apply_filter_button);
		applyFilterButton.setOnClickListener(this);
		
		// Inflate the layout for this fragment
		return view;
	}

	/*
	// TODO: Rename method, update argument and hook method into UI event
	public void onButtonPressed(Uri uri) {
		if (mListener != null) {
			mListener.applyFilterButtonClicked(uri);
		}
	}*/

	@Override
	public void onAttach(Activity activity) {
		super.onAttach(activity);
		try {
			mListener = (InventorySearchFragmentInteractionListener) activity;
		} catch (ClassCastException e) {
			throw new ClassCastException(activity.toString()
					+ " must implement InventorySearchFragmentInteractionListener");
		}
	}
	
	public void init()
	{
		layoutOfPopup = new LinearLayout(null);
		popupText.setText("invalid VIN");
		popupText.setPadding(0,  0,  0,  20);
		layoutOfPopup.setOrientation(1);
		layoutOfPopup.addView(popupText);
	}
	
	@SuppressWarnings("deprecation")
	public void popupInit()
	{
		popup = new PopupWindow(layoutOfPopup, LayoutParams.FILL_PARENT, LayoutParams.WRAP_CONTENT);
		popup.setContentView(layoutOfPopup);
	}

	@Override
	public void onDetach() {
		super.onDetach();
		mListener = null;
	}

	/**
	 * This interface must be implemented by activities that contain this
	 * fragment to allow an interaction in this fragment to be communicated to
	 * the activity and potentially other fragments contained in that activity.
	 * <p>
	 * See the Android Training lesson <a href=
	 * "http://developer.android.com/training/basics/fragments/communicating.html"
	 * >Communicating with Other Fragments</a> for more information.
	 */
	public interface InventorySearchFragmentInteractionListener {
		// TODO: Update argument type and name
		public void applyFilterButtonClicked();
	}

	@Override
    public void onClick(View v) {
		if(vinTextfield.getText().toString().length()!=10)
		{
			//create pop-up
			if(v.getId() == R.id.apply_filter_button)
			{
				popup.showAsDropDown(applyFilterButton, 0, 0);
			}
			else
			{
				popup.dismiss();
			}
		}
        Toast.makeText(this.getActivity(), "Searching for vehicle...", Toast.LENGTH_LONG).show();
        mListener.applyFilterButtonClicked();
    }

}
